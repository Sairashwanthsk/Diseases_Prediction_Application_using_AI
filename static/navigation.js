
// const sidebar = document.querySelector('.sidebar'),
// toggle = document.querySelector('.toggle');
//   searchBtn = body.querySelector('.search-box'),
//   modeSwitch = body.querySelector('.toggle-switch'),
//   modeText = body.querySelector('.mode-text')

// toggle.addEventListener('click', () => {
// sidebar.classList.toggle('close')
// })

// searchBtn.addEventListener('click', () => {
//   sidebar.classList.remove('close')
// })

// modeSwitch.addEventListener('click', () => {
//   body.classList.toggle('dark')

//   if (body.classList.contains('dark')) {
//     modeText.innerText = 'Light mode'
//   } else {
//     modeText.innerText = 'Dark mode'
//   }
// })
function sidebarClose(){
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('close');
}
function navHighlighter(){
    const sections = document.querySelectorAll('section'),
        sidenav = document.querySelectorAll('.menu .menu-links .nav-link a');
    let section_current =''; // Initializing current attribute for sidenav
    sections.forEach((section) => {
        section_current = section.getAttribute('id');  // current section is assigned, for sidenav menu items highlighter
    })

    //Section highlighter
    sidenav.forEach((a) => {
        a.classList.remove('active');
        if(a.classList.contains(section_current)){
            a.classList.add('active') //Set side navigation menu to active to highlight
        }
    })
}
