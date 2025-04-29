<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?= $site->title() ?></title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary-color: #6C63FF;
            --secondary-color: #f8f9fa;
            --text-color: #2d3436;
            --accent-color: #00b894;
            --shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Poppins', sans-serif;
            line-height: 1.6;
            color: var(--text-color);
            background-color: var(--secondary-color);
        }

        .container {
            max-width: 100%;
            padding: 1rem;
            margin: 0 auto;
        }

        header {
            background-color: var(--primary-color);
            color: white;
            padding: 1rem;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 1000;
            box-shadow: var(--shadow);
        }

        .header-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo {
            font-size: 1.5rem;
            font-weight: 600;
        }

        .nav-toggle {
            background: none;
            border: none;
            color: white;
            font-size: 1.5rem;
            cursor: pointer;
            padding: 0.5rem;
        }

        .nav-menu {
            display: none;
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background-color: white;
            padding: 1rem;
            box-shadow: var(--shadow);
            border-radius: 8px;
        }

        .nav-menu.active {
            display: block;
            animation: slideDown 0.3s ease;
        }

        .nav-menu a {
            color: var(--text-color);
            text-decoration: none;
            display: block;
            padding: 0.8rem;
            border-radius: 4px;
            transition: background-color 0.3s;
        }

        .nav-menu a:hover {
            background-color: var(--secondary-color);
        }

        main {
            margin-top: 5rem;
            padding: 1rem;
        }

        .card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: var(--shadow);
            transition: transform 0.3s;
        }

        .card:hover {
            transform: translateY(-5px);
        }

        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            margin-top: 2rem;
        }

        .feature-item {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            box-shadow: var(--shadow);
        }

        .feature-icon {
            font-size: 2rem;
            color: var(--primary-color);
            margin-bottom: 1rem;
        }

        .btn {
            display: inline-block;
            background-color: var(--primary-color);
            color: white;
            padding: 0.8rem 1.5rem;
            border-radius: 25px;
            text-decoration: none;
            font-weight: 500;
            transition: background-color 0.3s;
        }

        .btn:hover {
            background-color: #5a52d4;
        }

        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translateY(-10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @media (min-width: 768px) {
            .container {
                max-width: 768px;
            }

            .nav-toggle {
                display: none;
            }

            .nav-menu {
                display: flex;
                position: static;
                background: none;
                padding: 0;
                box-shadow: none;
            }

            .nav-menu a {
                color: white;
                margin-left: 1.5rem;
            }

            .nav-menu a:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <div class="header-content">
                <div class="logo"><?= $site->title() ?></div>
                <button class="nav-toggle">☰</button>
                <nav class="nav-menu">
                    <?php foreach ($site->children()->listed() as $item): ?>
                        <a href="<?= $item->url() ?>"><?= $item->title() ?></a>
                    <?php endforeach ?>
                </nav>
            </div>
        </div>
    </header>

    <main class="container">
        <div class="card">
            <?= $page->text()->kirbytext() ?>
        </div>

        <div class="feature-grid">
            <div class="feature-item">
                <div class="feature-icon">📱</div>
                <h3>Diseño Responsivo</h3>
                <p>Se adapta perfectamente a cualquier dispositivo</p>
            </div>
            <div class="feature-item">
                <div class="feature-icon">⚡</div>
                <h3>Rápido y Eficiente</h3>
                <p>Optimizado para una experiencia fluida</p>
            </div>
            <div class="feature-item">
                <div class="feature-icon">🎨</div>
                <h3>Diseño Moderno</h3>
                <p>Interfaz atractiva y fácil de usar</p>
            </div>
        </div>

        <div class="card" style="text-align: center;">
            <a href="#" class="btn">Comenzar Ahora</a>
        </div>
    </main>

    <script>
        document.querySelector('.nav-toggle').addEventListener('click', function() {
            document.querySelector('.nav-menu').classList.toggle('active');
        });
    </script>
</body>
</html> 