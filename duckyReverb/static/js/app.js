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




window.onload = function() {
    const mydata = JSON.parse(document.getElementById('mydata').textContent);
    console.log(mydata);
    console.log(mydata.colors);
    document.getElementById("albumImage").src = mydata.image;
    document.getElementById('title').textContent = mydata.name;
    document.getElementById('downloadButton').href = mydata.song;
    document.getElementById("audio").src =  mydata.song;
}