document.querySelectorAll('button[data-copy-target]').forEach(button => {
    button.addEventListener('click', function() {
        var targetSelector = this.getAttribute('data-copy-target');
        var input = document.querySelector(targetSelector);

        input.select();
        input.setSelectionRange(0, 99999);

        navigator.clipboard.writeText(input.value)
            .then(() => {
                console.log('Text copied!');
            })
            .catch(err => {
                console.error('Error: ', err)
                alert('Error!')
            });
    });
});