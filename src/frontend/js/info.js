function getInfo() {
  fetch("http://fuzzyguacamole.local:5000/api/v2/info",)
  .then(function (response) {
    return response.json();
  })
  .then(function (json) {
    document.querySelector(".info .position .posx").innerHTML = 'X: ' + json['pos']['x']
    document.querySelector(".info .position .posy").innerHTML = 'Y: ' + json['pos']['y']
    document.querySelector(".info .position .posz").innerHTML = 'Z: ' + json['pos']['z']

    document.querySelector(".info .temperature .bed").innerHTML = 'Bed: ' + json['bedTemp']
    document.querySelector(".info .temperature .nozzle").innerHTML = 'Nozzle: ' + json['nozzleTemp']

    currrentlyPrinting = document.querySelector(".info .currrentlyPrinting")
    currrentlyPrinting.removeChild(currrentlyPrinting.lastElementChild);

    if (json['printing']) {
      header = document.createElement('h5')
      header.innerHTML = 'Printing: ' + json['filename'];
      currrentlyPrinting.appendChild(header)
    } else {
      header = document.createElement('h5')
      header.innerHTML = 'No file currently printing';
      currrentlyPrinting.appendChild(header)
    }
    // console.log(json);
  })
  .catch(function (error) {
    document.getElementById('blocker').className = 'blocker';
    console.log("Error: " + error);
  });
}

getInfoInterval = setInterval(getInfo, 250)
