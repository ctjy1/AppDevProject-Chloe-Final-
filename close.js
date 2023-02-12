function closediv() {
    const rew_div = document.getElementById("reward-div");
//    const btn = document.getElementsByClassName('close-button')

    if (rew_div.style.display !== "none"){
        rew_div.style.display = "none";
    } else {
        rew_div.style.display = "block";
    };
}
