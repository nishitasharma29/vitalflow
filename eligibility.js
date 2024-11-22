function checkEligibility() {
    const age = document.getElementById('age').value;
    const weight = document.getElementById('weight').value;
    
    const health = document.querySelector('input[name="health"]:checked').value;
    const medications = document.querySelector('input[name="medications"]:checked').value;
    const surgery = document.querySelector('input[name="surgery"]:checked').value;
    const pregnancy = document.querySelector('input[name="pregnancy"]:checked').value;
    const tattoo = document.querySelector('input[name="tattoo"]:checked').value;
    const travel = document.querySelector('input[name="travel"]:checked').value;

    let result = '';

    if (
        age >= 18 && age <= 65 &&
        weight >= 50 &&
        health === 'yes' &&
        medications === 'no' &&
        surgery === 'no' &&
        pregnancy === 'no' &&
        tattoo === 'no' &&
        travel === 'no'
    ) {
        result = 'You are eligible to donate blood.';
    } else {
        result = 'You are not eligible to donate blood.';
    }

    document.getElementById('result').innerText = result;
}

