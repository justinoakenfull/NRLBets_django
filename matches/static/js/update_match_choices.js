document.addEventListener("DOMContentLoaded", function () {
    const locationChoices = document.getElementById("match_location").options;
    
    // Add event listeners for team selection and magic round checkbox
    document.querySelectorAll("input[name='home_team']").forEach((input) => {
        input.addEventListener("change", function () {
            updateLocationChoices(locationChoices);
        });
    });

    document.querySelectorAll("input[name='away_team']").forEach((input) => {
        input.addEventListener("change", function () {
            updateLocationChoices(locationChoices);
        });
    });

    document.getElementById("magic_round").addEventListener("change", function () {
        updateLocationChoices(locationChoices);
    });
});

function updateLocationChoices(locationChoices) {
    // Get the selected home and away teams
    const homeTeam = document.querySelector("input[name='home_team']:checked");
    const awayTeam = document.querySelector("input[name='away_team']:checked");
    const isMagicRound = document.getElementById("magic_round").checked;

    const homeTeamValue = homeTeam ? homeTeam.value : null;
    const awayTeamValue = awayTeam ? awayTeam.value : null;

    console.log("Home team: " + homeTeamValue);
    console.log("Away team: " + awayTeamValue);

    // Reset and update location choices
    for (let i = 0; i < locationChoices.length; i++) {
        const locationValue = locationChoices[i].value;

        // Default behavior: hide all locations
        locationChoices[i].style.display = "none";

        // Display locations matching home/away teams or their secondary/tertiary variants
        if (
            locationValue === homeTeamValue ||
            locationValue === awayTeamValue ||
            locationValue === `${homeTeamValue} SND` ||
            locationValue === `${awayTeamValue} SND` ||
            locationValue === `${homeTeamValue} TRD` ||
            locationValue === `${awayTeamValue} TRD`
        ) {
            locationChoices[i].style.display = "block";
            document.getElementById("match_location").value = locationChoices[i].value;
        }

        // Special case for Magic Round
        if (isMagicRound && locationValue.includes("BRI")) {
            locationChoices[i].style.display = "block";
            document.getElementById("match_location").value = locationChoices[i].value;
        }
    }
}
