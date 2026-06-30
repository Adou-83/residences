document.addEventListener("DOMContentLoaded", function(){

/* =========================
   CALENDRIER
========================= */

let calendarEl = document.getElementById('calendar');

if(calendarEl){
     let events = datesReservees.map(function(res){
        return {
            start: res.from,
            end: res.to,
            display: 'background',
            color: '#ff0000'
        }
    });

    let calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        locale: 'fr',
        height: 400,
        events: events
    });

    calendar.render();
}


/* =========================
   CALCUL PRIX
========================= */

let arrivee = document.getElementById("id_date_arrivee");
let depart = document.getElementById("id_date_depart");

let nbNuits = document.getElementById("nb_nuits");
let prixTotal = document.getElementById("prix_total");

function calculerPrix(){

    if(arrivee.value && depart.value){

        let dateArrivee = new Date(arrivee.value);
        let dateDepart = new Date(depart.value);

        let diff = dateDepart - dateArrivee;
        let nuits = diff / (1000 * 60 * 60 * 24);

        if(nuits > 0){

            nbNuits.innerText = nuits;
            prixTotal.innerText = nuits * prixParNuit;

        }
    }
}

if(arrivee && depart){

    arrivee.addEventListener("change", calculerPrix);
    depart.addEventListener("change", calculerPrix);

}


/* =========================
   WHATSAPP
========================= */

let whatsappBtn = document.getElementById("whatsapp-btn");

function updateWhatsAppLink(){

    let personnes = document.getElementById("id_personnes").value;

    let message = `Bonjour, je souhaite réserver la résidence ${nomResidence}

📍 Résidence : ${nomResidence}
📅 Arrivée : ${arrivee.value}
📅 Départ : ${depart.value}
👥 Personnes : ${personnes}`;

    let numero = "2250778485274";

    let url = `https://wa.me/${numero}?text=${encodeURIComponent(message)}`;

    whatsappBtn.href = url;

}

if(arrivee && depart && whatsappBtn){

    arrivee.addEventListener("change", updateWhatsAppLink);
    depart.addEventListener("change", updateWhatsAppLink);

}

let personnesInput = document.getElementById("id_personnes");

if(personnesInput){

    personnesInput.addEventListener("input", updateWhatsAppLink);

}

updateWhatsAppLink();

});