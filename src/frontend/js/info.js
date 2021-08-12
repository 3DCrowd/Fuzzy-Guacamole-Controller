function getInfo() {
  fetch("http://3dprinter.local:5000/api/v2/info",)
  .then(function (response) {
    return response.json();
  })
  .then(function (json) {
    document.querySelector(".info .position .posx").innerHTML = 'X: ' + json['pos']['x']
    document.querySelector(".info .position .posy").innerHTML = 'Y: ' + json['pos']['y']
    document.querySelector(".info .position .posz").innerHTML = 'Z: ' + json['pos']['z']

    document.querySelector(".info .temperature .bed").innerHTML = 'Bed: ' + json['bedTemp']
    document.querySelector(".info .temperature .nozzle").innerHTML = 'Nozzle: ' + json['nozzleTemp']
  })
  .catch(function (error) {
    console.log("Error: " + error);
  });
}

setInterval(getInfo, 250)
