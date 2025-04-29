<?php

// Obtener la ruta base del proyecto
$base_dir = dirname(dirname(dirname(__FILE__)));
$assets_dir = $base_dir . '/assets/juegos/dependencias';

// Crear directorio de dependencias si no existe
if (!file_exists($assets_dir)) {
    mkdir($assets_dir, 0777, true);
}

// Load Kirby
require $base_dir . '/kirby/bootstrap.php';

// Create Kirby instance
$kirby = new Kirby([
    'roots' => [
        'index'    => $base_dir,
        'base'     => $base_dir,
        'content'  => $base_dir . '/content',
        'site'     => $base_dir . '/site',
        'storage'  => $base_dir . '/storage',
        'accounts' => $base_dir . '/site/accounts',
        'cache'    => $base_dir . '/storage/cache',
        'sessions' => $base_dir . '/storage/sessions',
    ]
]);

// Render the page
echo $kirby->render(); 