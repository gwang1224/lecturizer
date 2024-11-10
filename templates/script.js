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

    // Check if the selected state is a one-party consent state
    if (onePartyStates.includes(selectedState)) {
        // Redirect to a new page
        window.location.href = 'consent-allowed.html';
    } else {
        alert("This is a two-party consent state. Recording requires both parties' consent.");
    }
}
