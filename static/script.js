document.getElementById('save-button').addEventListener('click', function() {
    let content = '';
    // Append the normalized exponents
    content += '1. Normalize Exponents\n';
    content += document.getElementById('1').innerText + '\n';
    content += document.getElementById('2').innerText + '\n';

    // Check if the GRS section should be included
    if (document.getElementById('3')) {
        content += '\n2. Perform Addition with Respect to G/R/S\n';
        content += document.getElementById('3').innerText + '\n';
        content += document.getElementById('4').innerText + '\n';
        content += document.getElementById('5').innerText + '\n';
    } else {
        content += '\n2. Perform Addition\n';
        content += document.getElementById('6').innerText + '\n';
        content += document.getElementById('7').innerText + '\n';
        content += document.getElementById('8').innerText + '\n';
    }

    content += '\n3. Rounded Final Answer\n';
    content += document.getElementById('9').innerText + '\n';

    // Create a blob with the content and type set to text/plain
    const blob = new Blob([content], { type: 'text/plain' });

    // Create a link element
    const link = document.createElement('a');

    // Set the download attribute with a filename
    link.download = 'output.txt';

    // Create an object URL for the blob
    link.href = URL.createObjectURL(blob);

    // Append the link to the body
    document.body.appendChild(link);

    // Programmatically click the link to trigger the download
    link.click();

    // Remove the link from the document
    document.body.removeChild(link);
});

document.getElementById('operand1').addEventListener('input', function(event) {
    const inputField = event.target;
    const errorMessage = document.getElementById('error-message1');
    const value = inputField.value;
    const binaryFloatPattern = /^[01]*(\.[01]+)?$/;

    if (binaryFloatPattern.test(value)) {
        // Valid binary floating point number
        inputField.setCustomValidity('');
        errorMessage.style.display = 'none';
    } else {
        // Invalid binary floating point number
        inputField.setCustomValidity('Invalid binary floating point number');
        errorMessage.style.display = 'block';
    }
});

document.getElementById('operand2').addEventListener('input', function(event) {
    const inputField = event.target;
    const errorMessage = document.getElementById('error-message2');
    const value = inputField.value;
    const binaryFloatPattern = /^-?[01]*(\.[01]+)?$/;

    if (binaryFloatPattern.test(value)) {
        // Valid binary floating point number
        inputField.setCustomValidity('');
        errorMessage.style.display = 'none';
    } else {
        // Invalid binary floating point number
        inputField.setCustomValidity('Invalid binary floating point number');
        errorMessage.style.display = 'block';
    }
});
