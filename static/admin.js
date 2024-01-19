function deleteUser(customerId){
    fetch('/delete-user',{
        method: 'POST',
        body: JSON.stringify({userId: customerId}),
    }).then((_res) =>{
	    window.locatin.href="/admin";
        window.location.reload();
    });
}

function toggleSlide(slideId) {
    var sliderContent = document.getElementById('sliderContent');
    let btnA=document.getElementById("user_btn")
    let btnB=document.getElementById("admin_btn")
    if (slideId === 'A') {
        sliderContent.style.transform = 'translateX(0)';
        btnA.classList.add("active");
        btnB.classList.remove("active");
    } else if (slideId === 'B') {
        sliderContent.style.transform = 'translateX(-100%)';
        btnB.classList.add("active");
        btnA.classList.remove("active");
    }
}