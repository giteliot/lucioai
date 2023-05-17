
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

const baseImg = new Image();
baseImg.src = `static/images/BASE.png`;

const crouchImg = new Image();
crouchImg.src = `static/images/CROUCH.png`;

const sitImg = new Image();
sitImg.src = `static/images/SIT.png`;

const jumpImgArr = [];
for (let k = 1; k <= 7; k++) {
      let jumpImg = new Image();
      jumpImg.src = `static/images/JUMP/JUMP${k}.png`;
      jumpImgArr.push(jumpImg);
}

const walkImgArr = [];
for (let k = 1; k <= 7; k++) {
      let walkImg = new Image();
      walkImg.src = `static/images/WALK/WALK${(k+1)%2+1}.png`;
      walkImgArr.push(walkImg);
}

const bgImg = new Image();
bgImg.src = `static/images/train_room_background.png`;

const images = {
      "BACKGROUND": bgImg,
      "BASE": baseImg,
      "CROUCH": [crouchImg],
      "JUMP": jumpImgArr,
      "SIT": [sitImg],
      "WALK": walkImgArr
};


function drawDefault() {
      ctx.drawImage(bgImg, 0, 0, canvas.width, canvas.height);      
      ctx.drawImage(images["BASE"], canvas.width/2-40, canvas.height-300, 180, 270);}

function drawAnimation(animationName) {
      console.log(`animating ${animationName}`);

      let frames = 7;

      let i = setInterval(
            () => {
                  let currentFrame = (images[animationName].length-frames)%images[animationName].length
                  if (frames < 0) {
                        clearInterval(i);
                        drawDefault();
                        return;
                  }

                  ctx.drawImage(bgImg, 0, 0, canvas.width, canvas.height);   
                  ctx.drawImage(images[animationName][currentFrame], canvas.width/2-40, canvas.height-300, 180, 270);
                  frames--;      
            }
            , 100);
      
      }

images["BACKGROUND"].onload = function() {
      setTimeout(drawDefault, 100);
}
