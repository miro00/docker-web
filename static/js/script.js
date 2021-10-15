document.querySelectorAll(".container-controls__button").forEach(btn => {
  btn.addEventListener("click", async (e) => {
    const btnType = e.currentTarget.classList[1]
    const containerId = e.currentTarget.closest(".container").id
    const container = document.getElementById(containerId)
    container.querySelectorAll(".container-controls__button").forEach(cbtn => {
      cbtn.disabled = false
    })
    e.currentTarget.disabled = true
    const res = await fetch("/commands", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        id: containerId,
        type: btnType
      })
    })    

    if (res.ok) {
      const oldStatus = container.querySelector(".container-status").classList.value.split(" ")[1]
      container.querySelector(".container-status").classList.remove(oldStatus)
    }
  })
})
