function getInfo() {
  fetch("http://fuzzyguacamole.local:5000/api/v2/info",)
  .then(function (response) {
    if (response.status != 200){
      console.log(response.status)
    }
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
    updateConnections()
    clearInterval(getInfoInterval)


    document.getElementById('blocker').className = 'blocker';
    // console.log("Error: " + error);
  });
}

function updateConnections() {
  fetch("http://fuzzyguacamole.local:5000/api/v2/connect/list")
  .then(function (response) {
      return response.json();
    })
    .then(function (json) {
      var connectionSelect = document.getElementById('connectionSelect')
      connectionSelect.innerHTML = ''
      for (port in json['ports']){
        option = document.createElement('option')
        option.value = json['ports'][port]
        option.innerHTML = json['ports'][port]

        connectionSelect.appendChild(option)
      }
    });
}

function reconnect(){
  requestJson = {
    'port': document.getElementById('connectionSelect').value,
    'baudrate': document.getElementById('baudSelect').value
  }
  document.body.style.cursor = "wait";
  document.getElementById('again').disabled = true;
  document.getElementById('refresh').disabled = true;

  fetch("http://fuzzyguacamole.local:5000/api/v2/connect", {
    method: 'POST',
    headers: {
    'Content-Type': 'application/json;charset=utf-8'
    },
    body: JSON.stringify(requestJson)
  }).then(function(response){
    console.log(response.status)

    if (response.status == 202){
      getInfoInterval = setInterval(getInfo, 250)
      document.getElementById('blocker').classList.remove('blocker')
      document.getElementById('blocker').classList.add('not-blocking')

      document.body.style.cursor = "default";
      document.getElementById('again').disabled = false;
      document.getElementById('refresh').disabled = false;
    } else {
      document.body.style.cursor = "default";
      document.getElementById('again').disabled = false;
      document.getElementById('refresh').disabled = false;
    }
  }
)
}

function pause() {
  var pause = document.getElementById('pause');
  var resume = document.getElementById('resume');

  if (resume.classList.contains('hidden')){
    fetch("http://fuzzyguacamole.local:5000/api/v2/control/pause", {
      method: 'POST',
      headers: {
      'Content-Type': 'application/json;charset=utf-8'
      },
    }).then(function(response){
      pause.classList.toggle('hidden');
      resume.classList.toggle('hidden');
    })
  } else {
    fetch("http://fuzzyguacamole.local:5000/api/v2/control/resume", {
      method: 'POST',
      headers: {
      'Content-Type': 'application/json;charset=utf-8'
      },
    }).then(function(response){
      pause.classList.toggle('hidden');
      resume.classList.toggle('hidden');
    })
  }
}

function stop() {
  fetch("http://fuzzyguacamole.local:5000/api/v2/control/stop", {
    method: 'POST',
    headers: {
    'Content-Type': 'application/json;charset=utf-8'
    },
  })
}

getInfoInterval = setInterval(getInfo, 250)
