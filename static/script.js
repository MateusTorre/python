// MODO ESCURO

const botaoTema = document.getElementById("tema-btn");

if (localStorage.getItem("tema") === "escuro") {
    document.body.classList.add("bg-dark", "text-light");
}

if (botaoTema) {
    botaoTema.addEventListener("click", () => {
        document.body.classList.toggle("bg-dark");
        document.body.classList.toggle("text-light");

        if (document.body.classList.contains("bg-dark")) {
            localStorage.setItem("tema", "escuro");
        } else {
            localStorage.setItem("tema", "claro");
        }
    });
}