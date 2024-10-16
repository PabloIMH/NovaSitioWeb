$(document).ready(function () {
    $('.fa-lock').click(function () {
        let input = $(this).siblings('input');
        if (input.attr('type') === 'password') {
            input.attr('type', 'text');
            $(this).toggleClass('fa-lock fa-eye');
        } else {
            input.attr('type', 'password');
            $(this).toggleClass('fa-eye fa-lock');
        }
    });

    // Capturar el evento 'Enter' en los campos de nombre de usuario y contraseña
    $('.form-control').keypress(function (e) {
        if (e.which == 13) {  // Código de tecla 'Enter'
            $('.log-btn').click();  // Simular clic en el botón "Acceder"
        }
    });

    $('.log-btn').click(function () {
        var valid = true;

        // Verificar si los campos están vacíos
        $('.form-group input').each(function () {
            if ($(this).val() === "") {
                valid = false;
                return false; // Salir del bucle si algún campo está vacío
            }
        });

        if (!valid) {
            // Añadir clase shake para el efecto de vibración si los campos no son válidos
            $('.login-form').addClass('shake');

            // Mostrar la alerta de error
            $('.alert').fadeIn(500).text('Por favor completa todos los campos');

            // Eliminar la clase shake después de la animación
            setTimeout(function () {
                $('.login-form').removeClass('shake');
            }, 500);

            // Desvanecer la alerta después de 3 segundos
            setTimeout(function () {
                $('.alert').fadeOut(500);
            }, 3000);
        } else {
            // Si el formulario es válido, envíalo
            $('form').submit();
        }
    });

    // Eliminar el estado de error si el usuario empieza a escribir
    $('.form-group input').keypress(function () {
        $('.alert').fadeOut(500);
    });
});
