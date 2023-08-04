const iomExpandButton = document.querySelector('.symptom-expand-button#iom');
const iomSymptomList = document.querySelector('.symptom-list#iom');
const cccExpandButton = document.querySelector('.symptom-expand-button#ccc');
const cccSymptomList = document.querySelector('.symptom-list#ccc');

iomExpandButton.addEventListener('click', () => {
  iomSymptomList.classList.toggle('closed');
  if (iomSymptomList.classList.contains('closed')) {
    iomExpandButton.innerHTML = "Click here to see more..."
  } else {
    iomExpandButton.innerHTML = "Click here to see less..."
  }
});

cccExpandButton.addEventListener('click', () => {
  cccSymptomList.classList.toggle('closed');
  if (cccSymptomList.classList.contains('closed')) {
    cccExpandButton.innerHTML = "Click here to see more..."
  } else {
    cccExpandButton.innerHTML = "Click here to see less..."
  }
});