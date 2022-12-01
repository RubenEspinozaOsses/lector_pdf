function checkIfPdf(){
    let files = Array.from(document.getElementById('formFileMultiple').files)
    let pdfs = files.filter(el => !el.name.endsWith('.pdf'));
    
    if (pdfs.length > 0) {
        alert('Subido archivo no pdf')
        document.getElementById('formFileMultiple').value = ''
    }
    
}

function mostrarTodo(){
    let tds = document.querySelectorAll('td')
    for(let td of tds){
        td.classList.remove('is-hidden')
    }
}

function buscar(){
    return
    let search = document.getElementById('search').value
    if (search.length < 4){
        return
    }

    if (search == '') {
        mostrarTodo();
        return
    }
    let tds = document.querySelectorAll('tr')

    for(let td of tds){
        if (!td.innerText.includes(search)){
            td.classList.add('is-hidden')
        }
    }

    console.log(td)
}