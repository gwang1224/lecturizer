// List of one-party consent states
const onePartyStates = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "Colorado", "District of Columbia",
    "Georgia", "Hawaii", "Idaho", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",
    "Maine", "Minnesota", "Mississippi", "Missouri", "Nebraska", "Nevada", "New Jersey",
    "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma",
    "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah",
    "Vermont", "Virginia", "West Virginia", "Wisconsin", "Wyoming"
];

function checkConsent() {
    const stateSelect = document.getElementById('stateSelect');
    const selectedState = stateSelect.value;
    const consentMessage = document.getElementById('consentMessage');

    if (onePartyStates.includes(selectedState)) {
        // Redirect to a new page for one-party consent states
        window.location.href = '/recording';
    } else {
        // Show two-party consent confirmation
        document.getElementById('twoPartyConsent').style.display = 'block';
    }
}

function confirmConsent(consentGiven) {
    const consentMessage = document.getElementById('consentMessage');

    if (consentGiven) {
        window.location.href = '/recording';
    } else {
        consentMessage.textContent = "This is a two-party consent state. Recording requires both parties' consent.";
        // alert("This is a two-party consent state. Recording requires both parties' consent.");
        document.getElementById('twoPartyConsent').style.display = 'none';
    }
}
