$('.output').hide()
resetInterface()
let command;
let action;
let shouldRecord = false;
let isSpeaking = false;
let commands = {}
let testWaves = [];
const THRESHOLD_SIMILARITY = 0.001;

function reward(isPositive) {
    action = undefined;
    command = undefined;
    shouldRecord = true;
    showReady();

    // reward_value = isPositive == true ? 1 : -1;
    // console.log("action="+action)
    // $.ajax({
    //     url: '/train',
    //     method: 'POST',
    //     data: {command: command, action: action, reward: reward_value},
    //     success: function(response) {
    //         action = undefined;
    //         command = undefined;
    //         $('.output').hide();
    //         $('.command-input').val("");
    //     }
    // });
    // shouldRecord = true;
    // showReady();
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

function getWaveMetric(wave) {
    const sum = wave.reduce((acc, cur) => acc + cur, 0);
    const mean = sum / wave.length;
    return wave.reduce((acc, cur) => acc + Math.pow(cur - mean, 2), 0) / (wave.length*wave.length);
}

function OLDgetWaveSimilarity(x, y) {
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

function getWaveSimilarity(x, y) {
    return Math.abs(x-y);
}

function findSimilarCommand(targetWave) {
    let selectedCmd;
    let maxSimilarity = THRESHOLD_SIMILARITY;
    for (const [cmd, waves] of Object.entries(commands)) {
        let avgSimilarity = waves.map((w) => getWaveSimilarity(w, targetWave))
            .reduce((x,y) => x+y)/waves.length;

        if (avgSimilarity <= maxSimilarity) {
            selectedCmd = cmd;
            maxSimilarity = avgSimilarity;
        }
    }

    return selectedCmd;
}


function updateAndGetNewCommand(wave) {
    wave = getWaveMetric(normalizeWave(wave));
    // testWaves.push(wave);
    console.log(wave);

    let memeorizedCommands = 0;
    for (let key in commands) {
        memeorizedCommands++;
    }
    let command;
    let numCommands = Object.keys(commands).length

    console.log(`used commands = ${numCommands}`)

    if (numCommands < 1) {
        console.log(`1- CMD1 CASE: COMMAND1`)
        command = "COMMAND1"; 
        commands[command] = [wave];
        return command;
    }
    
    let similarCommand = findSimilarCommand(wave);
    if (similarCommand != undefined) {
        console.log(`2- SIMILAR CASE: ${similarCommand}`)
        commands[similarCommand].push(wave);
        return similarCommand;
    }

    if (numCommands < 5) {
        console.log(`3- NEW CMD CASE: COMMAND${numCommands+1}`)
        command = "COMMAND"+(numCommands+1); 
        commands[command] = [wave];
        return command;
    }

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

    command = minKey;
    command[minKey] = [wave];
    console.log(`3- NEW CMD CASE: ${command}`)
    return command;
}
    

async function startListening() {
    showReady();
    shouldRecord = true;
    let wave = []
    const audioContext = new AudioContext();
    const mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mediaStreamSource = audioContext.createMediaStreamSource(mediaStream);

    const analyserNode = audioContext.createAnalyser();
    analyserNode.fftSize = 1024;
    mediaStreamSource.connect(analyserNode);

    const bufferLength = analyserNode.frequencyBinCount;
    const dataArray = new Float32Array(bufferLength);

    function processAudio() {
        if (isSpeaking == true && shouldRecord == true) {
            analyserNode.getFloatTimeDomainData(dataArray);
            wave.push(getEnergy(dataArray));
            // console.log(dataArray)
            //wave.push(dataArray);
            requestAnimationFrame(processAudio);
        }
    }

    function voiceStart() {
        if (shouldRecord == false) return;

        $('#record-screen').show();
        console.log('voice_start');
        wave = [];
        isSpeaking = true;
        requestAnimationFrame(processAudio);
    }

    function voiceStop() {
        if (shouldRecord == false) return;

        $('#record-screen').hide();
        console.log('voice_stop');
        isSpeaking = false;
        shouldRecord = false;
        command = JSON.stringify(wave);

        // $.ajax({
        //   url: '/command',
        //   method: 'POST',
        //   data: { wave: command},
        //   success: function(response) {
        //     action = response;
        //     console.log(`OUT: ${action}`);
        //     showReward();
        //     drawAnimation(action);
        //     }
        // });

        $.ajax({
          url: '/save',
          method: 'POST',
          data: { wave: command},
          success: function(response) {
            console.log(response);
            showReward();
            }
        });
    }

    const options = {
     source: mediaStreamSource,
     energy_threshold_ratio_pos: 5, // 5
     voice_stop: voiceStop, 
     voice_start: voiceStart
    }; 

    const vad = new VAD(options);
}

function stopAudioCapture() {
    console.log("stopping capture");
    shouldRecord = false
}

function resetInterface() {
      $('#starting-screen').show();
      $('#record-screen').hide();
      $('#reward-screen').hide();
}

function showReady() {
      $('#guide').html("Speak into the mic a command for lucio");
      $('#starting-screen').hide();
      $('#record-screen').hide();
      $('#reward-screen').hide();
}


function showReward() {
      $('#guide').html("Give treat or bonk lucio");
      $('#starting-screen').hide();
      $('#record-screen').hide();
      $('#reward-screen').show(); 
}

