$('.output').hide()
let command;
let action;
let shouldRecord = false;
let isSpeaking = false;
let commands = {}
const THRESHOLD_SIMILARITY = 25;

function reward(isPositive) {
    reward_value = isPositive == true ? 1 : -1;
    console.log("action="+action)
    $.ajax({
        url: '/train',
        method: 'POST',
        data: {command: command, action: action, reward: reward_value},
        success: function(response) {
            action = undefined;
            command = undefined;
            $('.output').hide();
            $('.command-input').val("");
        }
    });
}

function showAction(action) {
    console.log(action)
    const img = $(".lucio-img");

    img.attr("src", `static/images/${action}.gif`);
    setTimeout(() => {img.attr("src", `static/images/lucio_base.png`);}, 1200) 
}


function handleKeyDown(event) {

    if (event.keyCode === 13 && !action) { // 13 is the code for "Enter" key
      event.preventDefault(); // prevent the default behavior of the "Enter" key
      $.ajax({
      url: '/command',
      method: 'GET',
      data: {command: $('.command-input').val()},
      success: function(response) {
        action = response;
        $('.output').show()
        showAction(response)
        }
      });
    }
}

function getEnergy(buffer) {
  let sum = 0;
  for (let i = 0; i < buffer.length; i++) {
    sum += buffer[i] * buffer[i];
  }
  return sum / buffer.length;
}


function normalizeWave(wave) {
    const sum = wave.reduce((acc, cur) => acc + cur, 0);
    const mean = sum / wave.length;
    const variance = wave.reduce((acc, cur) => acc + Math.pow(cur - mean, 2), 0) / wave.length;
    const standardDeviation = Math.sqrt(variance);

    return wave.map((x) => (x - mean) / standardDeviation);
}

function getWaveSimilarity(x, y) {
    // Normalize the waveforms
    let x_mean = x.reduce((a, b) => a + b) / x.length;
    let y_mean = y.reduce((a, b) => a + b) / y.length;
    let x_std = Math.sqrt(x.reduce((a, b) => a + (b - x_mean) ** 2, 0) / x.length);
    let y_std = Math.sqrt(y.reduce((a, b) => a + (b - y_mean) ** 2, 0) / y.length);
    x = x.map(val => (val - x_mean) / x_std);
    y = y.map(val => (val - y_mean) / y_std);

    // Compute cross-correlation
    let corr = new Array(x.length + y.length - 1).fill(0);
    for (let i = 0; i < x.length; i++) {
        for (let j = 0; j < y.length; j++) {
            corr[i + j] += x[i] * y[j];
        }
    }

    // Find lag value with highest correlation
    let lag = corr.indexOf(Math.max(...corr)) - (x.length - 1);
    return corr[corr.indexOf(Math.max(...corr))];
}

function findSimilarCommand(targetWave) {
    let selectedCmd;
    let maxSimilarity = THRESHOLD_SIMILARITY;
    for (const [cmd, waves] of Object.entries(commands)) {
        let avgSimilarity = waves.map((w) => getWaveSimilarity(w, targetWave))
            .reduce((x,y) => x+y)/waves.length;

        if (avgSimilarity > maxSimilarity) {
            selectedCmd = cmd;
            maxSimilarity = avgSimilarity;
        }
    }

    return selectedCmd;
}


function updateAndGetNewCommand(wave) {
    wave = normalizeWave(wave);

    let memeorizedCommands = 0;
    for (let key in commands) {
        memeorizedCommands++;
    }
    let command;
    let numCommands = Object.keys(commands).length

    console.log(`used commands = ${numCommands}`)

    if (numCommands < 1) {
        console.log("1- CMD1 CASE")
        command = "COMMAND1"; 
        commands[command] = [wave];
        return command;
    }
    
    let similarCommand = findSimilarCommand(wave);
    if (similarCommand != undefined) {
        console.log("2- SIMILAR CASE")
        commands[similarCommand].push(wave);
        return similarCommand;
    }

    if (numCommands < 5) {
        console.log("3- NEW CMD CASE")
        command = "COMMAND"+(numCommands+1); 
        commands[command] = [wave];
        return command;
    }
    console.log("4-REPLACE CMD CASE")
    let minKey;
    let minVal;
    for (let key in commands) {
        let curVal = commands[key]
        if (!minKey) {
            minKey = key;
            minVal = curVal.length;
            continue;
        } 

        if (minVal > curVal) {
            minKey = key;
            minVal = curVal;
        }
    }
}
    

async function startListening() {
    shouldRecord = true;
    let wave = []
    const audioContext = new AudioContext();
    const mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mediaStreamSource = audioContext.createMediaStreamSource(mediaStream);

    const analyserNode = audioContext.createAnalyser();
    analyserNode.fftSize = 2048;
    mediaStreamSource.connect(analyserNode);

    const bufferLength = analyserNode.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);

    function processAudio() {
        if (isSpeaking == true) {
            analyserNode.getByteTimeDomainData(dataArray);
            wave.push(getEnergy(dataArray));
            requestAnimationFrame(processAudio);
        }
    }

    function voiceStart() {
        if (shouldRecord == true) {
            console.log('voice_start');
            wave = [];
            isSpeaking = true;
            requestAnimationFrame(processAudio);
        }
    }

    function voiceStop() {
        console.log('voice_stop');
        isSpeaking = false;
        command = updateAndGetNewCommand(wave);
        console.log(`IN: ${command}`);

        $.ajax({
          url: '/command',
          method: 'GET',
          data: {command: command},
          success: function(response) {
            action = response;
            console.log(`OUT: ${action}`);
            $('.output').show()
            showAction(response)
            }
          });
    }

    const options = {
     source: mediaStreamSource,
     energy_threshold_ratio_pos: 15,
     voice_stop: voiceStop, 
     voice_start: voiceStart
    }; 

    const vad = new VAD(options);
}

function stopAudioCapture() {
    console.log("stopping capture");
    shouldRecord = false
}
