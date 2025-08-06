const inputs = document.querySelectorAll(".verify__inputs input");

inputs.forEach((input, index) => {
  input.addEventListener("input", (e) => {
    const value = e.target.value;
    if (/^[0-9]$/.test(value)) {
      if (index < inputs.length - 1) {
        inputs[index + 1].focus();
      }
    } else {
      e.target.value = "";
    }
  });

  input.addEventListener("keydown", (e) => {
    if (e.key === "Backspace" && !input.value && index > 0) {
      inputs[index - 1].focus();
    }
    if (e.key === "ArrowLeft" && index > 0) {
      inputs[index - 1].focus();
    }
    if (e.key === "ArrowRight" && index < inputs.length - 1) {
      inputs[index + 1].focus();
    }
  });
});