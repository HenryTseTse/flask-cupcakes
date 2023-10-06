const BASE_URL = "http://localhost:5000/api";

/** Generate Cupcake Through Form */

function generateCupcakeHTML(cupcake) {
    return `
        <div data-cupcake-id=${cupcake.id}>
            <li>
                ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
                <button class="delete-button>X</button>
            </li>
            <img class="Cupcake-img"
                src="${cupcake.image}"
                alt="(Image N/A)">
        </div>
    `;
}

/** Initial Cupcakes */

async function ShowInitialCupcakes() {
    const response = await axios.get(`${BASE_URL}/cupcakes`);

    for(let cupcake of response.data.cupcakes) {
        let newCupcake = $(generateCupCakeHTML(cupcake));
        $("#cupcake-list").append(newCupcake);
    }
}

/** Add Cupcake */

$("#new-cupcake-form").on("submit", async function (e) {
    e.preventDefault();
    let flavor = $("#form-flavor").val();
    let size = $("#form-size").val();
    let rating = $("#form-rating").val();
    let image = $("form-image").val();

    let response = await axios.post(`${BASE_URL}/cupcakes`, {
        flavor,
        size,
        rating,
        image,
    });
    let newCupcake = $(generateCupcakeHTML(response.data.cupcake));
    $("#cupcake-list").append(newCupcake);
    $("#new-cupcake-form").trigger("reset");
});


/** Delete Cupcake */

async function deleteButton(evt) {
    evt.preventDefault();
    let $cupcake = $(evt.target).closest("div");
    let cupcakeId = $cupcake.attr("data-cupcake-id");

    response = await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
    $cupcake.remove();
}

$("#cupcake-list").on("click", "delete-button", deleteButton);
$(ShowInitialCupcakes);