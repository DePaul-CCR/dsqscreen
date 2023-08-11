const checked = (el) => el.checked
const nextButton = document.querySelector('.next-question-button')

if(document.querySelector('.single-question-container')) {
  const radios = Array.from(document.querySelectorAll('input[type=radio]'))
  document.addEventListener('change', (e) => {
    console.log(e)
    if (radios.some(checked)) {
      nextButton.classList.remove('disabled')
    } else {
      debugger
      nextButton.classList.add('disabled')
    }
  })
} else {
  const leftFieldSet = document.querySelector('#left fieldset');
  const leftRadios = Array.from(leftFieldSet.querySelectorAll('input[type=radio]'))
  const rightFieldSet = document.querySelector('#right fieldset');
  const rightRadios = Array.from(rightFieldSet.querySelectorAll('input[type=radio]'))

  document.addEventListener('change', (e) => {
    if (leftRadios.some(checked) && rightRadios.some(checked)) {
      nextButton.classList.remove('disabled')
    } else {
      nextButton.classList.add('disabled')
    }
  })
}