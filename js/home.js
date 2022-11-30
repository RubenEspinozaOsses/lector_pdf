function checkIfPdf(){
    let files = Array.from(document.getElementById('formFileMultiple').files)
    let pdfs = files.filter(el => !el.name.endsWith('.pdf'));
    
    if (pdfs.length > 0) {
        alert('Subido archivo no pdf')
        document.getElementById('formFileMultiple').value = ''
    }
    
}