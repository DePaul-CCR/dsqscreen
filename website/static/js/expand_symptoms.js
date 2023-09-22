const iomExpandButton = document.querySelector('.symptom-expand-button#iom');
const iomSymptomList = document.querySelector('.symptom-list#iom');
const cccExpandButton = document.querySelector('.symptom-expand-button#ccc');
const cccSymptomList = document.querySelector('.symptom-list#ccc');
const meiccExpandButton = document.querySelector('.symptom-expand-button#meicc');
const meiccSymptomList = document.querySelector('.symptom-list#meicc');

function addExpandableFunction(expandButton, symptomList) {
  expandButton.addEventListener('click', () => {
    symptomList.classList.toggle('closed');
    expandButton.classList.toggle('closed');
    if (symptomList.classList.contains('closed')) {
      expandButton.innerHTML = "Click here to see more..."
    } else {
      expandButton.innerHTML = "Click here to see less..."
    }
  });  
}

addExpandableFunction(iomExpandButton, iomSymptomList)
addExpandableFunction(cccExpandButton, cccSymptomList)
addExpandableFunction(meiccExpandButton, meiccSymptomList)