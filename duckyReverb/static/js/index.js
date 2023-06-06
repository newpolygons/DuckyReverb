/*
Copyright (c) 2023 NewPolygons.

This file is part of DuckyReverb.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/





let timer;

document.addEventListener('input', e => {
  const el = e.target;
  
  if( el.matches('[data-color]') ) {
    clearTimeout(timer);
    timer = setTimeout(() => {
      document.documentElement.style.setProperty(`--color-${el.dataset.color}`, el.value);
    }, 100)
  }
})




window.onload = function() {
  const mydata = JSON.parse(document.getElementById('mydata').textContent);
  console.log(mydata.colors);
  document.getElementById("albumImage").src = mydata.image;
  document.getElementById('title').textContent = mydata.name;
  document.getElementById('downloadButton').href = mydata.song;

  var isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent);
  if (isIOS) {

  } else {
    coolStuff();
  };
  

  
  };
  var isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent);
  var ranBefore = false;
  if (isIOS) {
    
  
  document.addEventListener('touchstart',  function () {
    
    if (ranBefore === false) {
      document.getElementsByTagName('audio')[0].play();
      document.getElementsByTagName('audio')[0].pause();
      coolStuff();
      ranBefore = true;
    }
    
});
  };


function coolStuff() {
    const mydata = JSON.parse(document.getElementById('mydata').textContent);
    var file =  mydata.song;
    var audio = document.getElementById("audio");
  
    
    audio.src = file;
    console.log(audio.src)
    audio.load();
    var context = new AudioContext();
    var src = context.createMediaElementSource(audio);
    var analyser = context.createAnalyser();

    var canvas = document.getElementById("canvas");
    
    canvas.width = window.innerWidth / 1.3;
    canvas.height = window.innerHeight / 3.5;
    var ctx = canvas.getContext("2d");

    src.connect(analyser);
    analyser.connect(context.destination);

    analyser.fftSize = 256;

    var bufferLength = analyser.frequencyBinCount;
    console.log(bufferLength);

    var dataArray = new Uint8Array(bufferLength);

    var WIDTH = canvas.width;
    var HEIGHT = canvas.height;
    
    var barWidth = (WIDTH / bufferLength) * 2.5;
    var barHeight;
    var x = 0;

    function renderFrame() {
      requestAnimationFrame(renderFrame);

      x = 0;

      analyser.getByteFrequencyData(dataArray);

      ctx.fillStyle = "#FFFFFF";
      ctx.fillRect(0, 0, WIDTH, HEIGHT);

      for (var i = 0; i < bufferLength; i++) {
        barHeight = dataArray[i];
        barHeight = barHeight - 50;
        //console.log(barHeight)
        var r = mydata.colors[0]
        var g = mydata.colors[1]
        var b = mydata.colors[2]

        ctx.fillStyle = "rgb(" + r + "," + g + "," + b + ")";
        ctx.fillRect(x, HEIGHT - barHeight, barWidth, barHeight);

        x += barWidth + 1;
      }
    }

    //audio.play();
    renderFrame();
  };

