console.log("script linked")

function addsighting(event){
    event.preventDefault()
    console.log("form submitted")

    const form = document.querySelector("#new_sighting")
    let formData = new FormData(form)

    fetch('/api/sighting/create', {
        method: 'post',
        body: formData
    })
    .then(res => res.json())
    .then(data => {console.log(data)
        console.log(data)
        let tableBody = document.querySelector("#table_body")
        tableBody.innerHTML += `
        <tr>
        <td>${data.data.location}</td>
        <td>${data.data.sighting_date}</td>
        <td>${data.user_name}</td>
        <td>
            <a href="/sighting/${data.id}/edit">Edit</a>
            <a href="/sighting/${data.id}/delete">Delete</a>
            <a href="/sighting/${data.id}/view">View</a>
        </td>
        </tr>
    `
    form.location.value = "";
    form.sighting_date.value = "";
    form.what_happened.value = "";
    form.number_of.value = "";
})}