const swiper = new Swiper('.swiper', {
  observer: true,
  observeParents: true,
  loop: true,
  pagination: {
    el: '.swiper-pagination',
    clickable: true
  },
});

let tabsBtn = document.querySelectorAll('.stages_item');
let tabsItem = document.querySelectorAll('.stage');

tabsBtn.forEach(function (element) {
  element.addEventListener('click', function (e) {
    const path = e.currentTarget.dataset.path;

    tabsBtn.forEach(function (btn) { btn.classList.remove('stages_item--active') });
    e.currentTarget.classList.add('stages_item--active');

    tabsItem.forEach(function (element) { element.classList.remove('stage--active') });
    document.querySelector(`[data-target="${path}"]`).classList.add('stage--active');
  })
})

new Accordion('.accordion-container')

let buger = document.querySelector('.burger');
let menu = document.querySelector('.header__nav');
let menuLinks = menu.querySelectorAll('.nav__link');

buger.addEventListener('click', function () {

  buger.classList.toggle('burger--active');
  menu.classList.toggle('header__nav--active');

  document.body.classList.toggle('stop-scroll');

})

menuLinks.forEach(function (el) {
  el.addEventListener('click', function () {

    buger.classList.remove('burger--active');
    menu.classList.remove('header__nav--active');
    document.body.classList.remove('stop-scroll')
  })
})

let searchbtn = document.querySelector('.search-start');
let searchform = document.querySelector('.header-form');
let closebtn = document.querySelector('.close');

searchbtn.addEventListener('click', function () {

  searchbtn.classList.toggle('search_btn--active');
  searchform.classList.toggle('header__form--active');
})

closebtn.addEventListener('click', function () {

  searchbtn.classList.remove('search_btn--active');
  searchform.classList.remove('header__form--active');
})