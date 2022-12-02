const add_other_income = document.getElementById("add_other_income")
const inputs = document.getElementById("inputs")

const current_date = () => {
    const now = new Date()
    return `${now.getFullYear()}-${now.getMonth() + 1}-${now.getDate() >= 10 ? now.getDate() : '0' + now.getDate()}`
}

function htmlToElement(html) {
    var template = document.createElement('template');
    html = html.trim(); // Never return a text node of whitespace as the result
    template.innerHTML = html;
    return template.content.firstChild;
}

const inputs_html = `
    <div class="input-group mt-2">
        <span class="input-group-text br-8px"><i class="fa-regular fa-align-left"></i></span>
        <input type="text" name="concept" class="form-control br-8px" placeholder="Concept" aria-label="concept" required>
        <span class="input-group-text">$</span>
        <input type="number" name="amount" class="form-control br-8px" placeholder="0.00" aria-label="amount" min="100" step="0.25" pattern="^\d*(\.\d{0,2})?$" required>
        <span class="input-group-text"><i class="fa-regular fa-calendar"></i></span>
        <input type="date" class="form-control br-8px" value="${current_date()}" aria-label="created_at" readonly>
    </div>
`
const max = 12

add_other_income.onclick = (event) => {
    event.preventDefault();
    if (!is_max_income_list(max)) {
        inputs.appendChild(htmlToElement(inputs_html))
        update_localstorage()
        if (is_max_income_list(max)) {
            add_other_income.style.display = "none"
        }
    }
}

const is_max_income_list = (max) => {
    const income_count = Number(localStorage.getItem("income_count") || 1)
    return income_count === max
}

const update_localstorage = () => {
    localStorage.setItem("income_count", (Number(localStorage.getItem("income_count")) || 1) + 1)
}

const reset_localstorage = () => {
    localStorage.setItem("income_count", 0)
}

reset_localstorage()
