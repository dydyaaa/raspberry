document.addEventListener('DOMContentLoaded', function() {
    var input = document.getElementById('username'); // Замените 'your_input_id' на id вашего input
    var mask = '00X0000';

    input.addEventListener('input', function(e) {
        var value = e.target.value;
        var maskedValue = '';
        var valueIndex = 0;

        for (var i = 0; i < mask.length; i++) {
            var maskChar = mask[i];

            if (maskChar === '0' && /^\d$/.test(value[valueIndex])) {
                maskedValue += value[valueIndex++];
            } else if (maskChar === 'X' && /^[a-zA-Z]$/.test(value[valueIndex])) {
                maskedValue += value[valueIndex++];
            } else if (maskChar === value[valueIndex]) {
                maskedValue += value[valueIndex++];
            } else {
                break;
            }
        }

        e.target.value = maskedValue;
    });
});