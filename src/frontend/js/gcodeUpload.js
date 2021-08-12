const dropArea = document.querySelector('.drag-area');
const dragText = document.querySelector('.header');

let button = dropArea.querySelector('.button');
let input = dropArea.querySelector('input');

let file;

dropArea.addEventListener('dragover', (event) => {
  event.preventDefault();
  dropArea.classList.add('active');
  dragText.textContent = 'Release to Upload';
});

dropArea.addEventListener('dragleave', () => {
  dropArea.classList.remove('active');
  dragText.textContent = 'Drag & Drop';
});

dropArea.addEventListener('drop', (event) => {
  event.preventDefault();
  file = event.dataTransfer.files[0];

  displayFile();
});

button.onclick = () => {
  input.click();
};

input.addEventListener('change', function () {
  file = this.files[0];

  displayFile();
});

function displayFile(){
  validExtension = 'text/x.gcode';

  if (file.type == validExtension) {
    dropArea.innerHTML = '<span class="header"> "' + file.name + '" successfully uploaded </span>';
  } else {
    dropArea.removeChild(dropArea.lastElementChild);

    html = document.createElement('span');
    html.textContent = '"' + file.name + '"is not a .gcode file'
    html.style.color = 'red';
    dropArea.append(html);
  }
}

function sendfile() {
  const formData  = new FormData();
  formData.append('file', file);

  const options = {
    method: 'POST',
    body: formData,
  }

  fetch("http://3dprinter.local:5000/api/v2/print/gcode", options)
  .then(function (response) {
    return response.json();
  })
  .then(function (myJson) {
    console.log(myJson);
  })
  .catch(function (error) {
    console.log("Error: " + error);
  });
}
