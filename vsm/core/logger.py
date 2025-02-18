"""
Module: logger
Description: Implémente une classe Logger en Python qui gère à la fois l'affichage
             de logs (avec couleur et horodatage) et l'écriture dans un fichier de log.
             Les anciens fichiers de log sont archivés automatiquement dans un fichier ZIP.
             De plus, les logs écrits dans le fichier sont plus détaillés (1 niveau en plus)
             que ceux affichés en console.
Auteur: By Gabin Degrange - 2025
"""

import os
import sys
import time
import zipfile
from datetime import datetime
from typing import Callable, Optional


class Logger:
    """
    Logger avec gestion de niveaux (DEBUG, INFO, WARNING, ERROR) et horodatage.
    
    Caractéristiques :
      - Affichage en console avec couleurs selon un seuil défini par `level`.
      - Écriture des logs dans le fichier "log/latest.log" avec un seuil un cran inférieur
        afin d'obtenir un niveau de détail supplémentaire.
      - Archivage automatique des logs existants dans le dossier "log/old" sous forme de ZIP.
      - Méthodes statiques pour afficher une barre de chargement pouvant suivre un phénomène réel
        (via un callback) et pour afficher un écran de démarrage.
    """

    # Codes ANSI pour les couleurs par niveau
    COLORS = {
        "DEBUG": "\033[96m",    # Cyan
        "INFO": "\033[92m",     # Vert
        "WARNING": "\033[93m",  # Jaune
        "ERROR": "\033[91m",    # Rouge
        "RESET": "\033[0m",     # Réinitialiser la couleur
    }

    LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR"]

    # Chemin du fichier de log actuel et du dossier d'archives
    LOG_FILE = os.path.join("log", "latest.log")
    ARCHIVE_DIR = os.path.join("log", "old")

    def __init__(self, level: str = "DEBUG") -> None:
        """
        Initialise le logger avec un niveau minimal pour l'affichage console et prépare
        le fichier de log avec un seuil un cran inférieur pour une trace plus détaillée.
        
        Args:
            level (str): Niveau minimal des messages à afficher dans la console.
                         (DEBUG, INFO, WARNING, ERROR)
        Raises:
            ValueError: Si le niveau passé n'est pas valide.
        """
        if level not in self.LEVELS:
            raise ValueError(f"Le niveau '{level}' n'est pas valide. Choisissez parmi {self.LEVELS}.")
        self.level = level

        # Déterminer le niveau pour le fichier de log (un cran plus bas pour plus de détails)
        level_index = self.LEVELS.index(level)
        if level_index == 0:
            self.file_level = level  # DEBUG est le niveau le plus bas
        else:
            self.file_level = self.LEVELS[level_index - 1]

        # S'assurer que le dossier "log" existe
        log_dir = os.path.dirname(self.LOG_FILE)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Gestion de l'archivage du log existant
        self._archive_existing_log()

        # Ouvrir le fichier de log en mode ajout (utf-8)
        self.log_file = open(self.LOG_FILE, "a", encoding="utf-8")

    def _archive_existing_log(self) -> None:
        """
        Si un fichier de log existant est présent, le zipper dans le dossier ARCHIVE_DIR
        avec un nom basé sur le timestamp, puis le supprimer.
        """
        if os.path.exists(self.LOG_FILE):
            # Créer le dossier d'archives s'il n'existe pas.
            if not os.path.exists(self.ARCHIVE_DIR):
                os.makedirs(self.ARCHIVE_DIR)
            # Générer un nom d'archive à partir de la date actuelle
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_name = os.path.join(self.ARCHIVE_DIR, f"{timestamp}.zip")
            with zipfile.ZipFile(archive_name, "w", zipfile.ZIP_DEFLATED) as zipf:
                # Utiliser arcname pour ne pas inclure tout le chemin dans l'archive
                zipf.write(self.LOG_FILE, arcname=os.path.basename(self.LOG_FILE))
            os.remove(self.LOG_FILE)

    def _get_timestamp(self) -> str:
        """
        Retourne l'heure actuelle sous forme de chaîne formatée.
        
        Returns:
            str: Timestamp sous le format "YYYY-MM-DD HH:MM:SS"
        """
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _should_log_console(self, msg_level: str) -> bool:
        """
        Vérifie si le message doit être affiché en console selon le niveau courant.
        
        Args:
            msg_level (str): Niveau du message à logger.
        
        Returns:
            bool: True si le message doit être affiché en console, False sinon.
        """
        return self.LEVELS.index(msg_level) >= self.LEVELS.index(self.level)

    def _should_log_file(self, msg_level: str) -> bool:
        """
        Vérifie si le message doit être enregistré dans le fichier de log selon le niveau
        un cran inférieur au niveau courant.
        
        Args:
            msg_level (str): Niveau du message à logger.
        
        Returns:
            bool: True si le message doit être enregistré dans le fichier, False sinon.
        """
        return self.LEVELS.index(msg_level) >= self.LEVELS.index(self.file_level)

    def _write_to_file(self, text: str) -> None:
        """
        Écrit une ligne dans le fichier de log et force le flush pour l'écriture immédiate.
        
        Args:
            text (str): Le texte à écrire dans le fichier de log.
        """
        self.log_file.write(text + "\n")
        self.log_file.flush()

    def log(self, level: str, message: str) -> None:
        """
        Affiche et enregistre un message avec son niveau et timestamp.
        
        Le message est affiché en console si son niveau est supérieur ou égal à `self.level`
        et est écrit dans le fichier de log si son niveau est supérieur ou égal à `self.file_level`.
        Le format du message est : "[timestamp] [LEVEL] message"
        
        Args:
            level (str): Niveau du message.
            message (str): Contenu du message à logger.
        """
        timestamp = self._get_timestamp()
        formatted_message = f"[{timestamp}] [{level}] {message}"
        if self._should_log_console(level):
            color = self.COLORS.get(level, self.COLORS["RESET"])
            print(f"{color}{formatted_message}{self.COLORS['RESET']}")
        if self._should_log_file(level):
            self._write_to_file(formatted_message)

    def debug(self, message: str) -> None:
        """Log un message de niveau DEBUG."""
        self.log("DEBUG", message)

    def info(self, message: str) -> None:
        """Log un message de niveau INFO."""
        self.log("INFO", message)

    def warning(self, message: str) -> None:
        """Log un message de niveau WARNING."""
        self.log("WARNING", message)

    def error(self, message: str) -> None:
        """Log un message de niveau ERROR."""
        self.log("ERROR", message)

    @staticmethod
    def show_loading_bar(total: int = 50,
                         prefix: str = "Chargement",
                         suffix: str = "Terminé",
                         length: int = 50,
                         fill: str = "█",
                         sleep_time: float = 0.05,
                         progress_callback: Optional[Callable[[], float]] = None,
                         integrate: bool = False,
                         start_time: Optional[float] = None) -> None:
        """
        Affiche une barre de chargement interactive dans le terminal.
        
        Deux modes sont possibles :
          - Si `progress_callback` est fourni, il s'agit d'une fonction renvoyant un float
            compris entre 0.0 et 1.0 indiquant l'avancement réel d'un phénomène.
          - Sinon, la barre simule une progression via une boucle avec un sleep.
        
        Le paramètre `integrate` permet de choisir entre deux modes d'affichage :
          - integrate=False : la barre reste affichée à la fin.
          - integrate=True  : la barre est effacée à la fin et, si `start_time` est fourni,
                            un message [INFO] indiquant la durée du processus est affiché.
        
        Args:
            total (int): Nombre d'étapes pour la simulation (non utilisé si progress_callback est défini).
            prefix (str): Texte affiché avant la barre.
            suffix (str): Texte affiché après la barre.
            length (int): Longueur de la barre.
            fill (str): Symbole indiquant la progression.
            sleep_time (float): Temps d'attente entre chaque mise à jour (en secondes).
            progress_callback (Optional[Callable[[], float]]): Fonction renvoyant le progrès (entre 0.0 et 1.0).
            integrate (bool): Si True, la barre est effacée à la fin et un message [INFO] avec la durée est affiché.
            start_time (Optional[float]): Heure de début (issue de time.time()) pour calculer la durée.
        """
        last_line = ""
        if progress_callback is not None:
            # Suivi du phénomène réel via le callback.
            while True:
                progress = progress_callback()
                progress = min(progress, 1.0)
                filled_length = int(length * progress)
                percent = progress * 100
                line = f'\r{prefix} |{fill * filled_length + "-" * (length - filled_length)}| {percent:.1f}% {suffix}'
                last_line = line
                sys.stdout.write(line)
                sys.stdout.flush()
                if progress >= 1.0:
                    break
                time.sleep(sleep_time)
        else:
            # Mode simulation classique
            for i in range(total + 1):
                progress = i / float(total)
                percent = progress * 100
                filled_length = int(length * i // total)
                line = f'\r{prefix} |{fill * filled_length + "-" * (length - filled_length)}| {percent:.1f}% {suffix}'
                last_line = line
                sys.stdout.write(line)
                sys.stdout.flush()
                time.sleep(sleep_time)
        
        # Gestion de l'affichage en mode intégré
        if integrate:
            if start_time is not None:
                duration = time.time() - start_time
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                info_message = f"[{timestamp}] [INFO] Processus terminé en {duration:.1f} secondes."
                sys.stdout.write('\r' + ' ' * len(last_line) + '\r')
                print(info_message)
            else:
                sys.stdout.write('\r' + ' ' * len(last_line) + '\r')
        else:
            print()  # Passage à la ligne après la barre

    @staticmethod
    def show_starting_screen() -> None:
        """
        Affiche un écran de démarrage en ASCII art.
        Le design affiche la mention **AUTO VSM** ainsi que la signature **By Gabin Degrange - 2025**.
        """
        starting_screen = r"""
╔══════════════════════════════════════════════════════╗
║    █████╗   ██╗   ██╗ ████████╗   ██████╗            ║
║   ██╔══██╗  ██║   ██║ ╚══██╔══╝  ██╔═══██╗           ║
║   ███████║  ██║   ██║    ██║     ██║   ██║           ║
║   ██╔══██║  ██║   ██║    ██║     ██║   ██║           ║
║   ██║  ██║  ╚██████╔╝    ██║     ╚██████╔╝           ║
║   ╚═╝  ╚═╝   ╚═════╝     ╚═╝      ╚═════╝            ║
║                                                      ║
║                    ██╗   ██╗  ███████╗  ███╗   ███╗  ║
║                    ██║   ██║  ██╔════╝  ████╗ ████║  ║
║                    ╚██╗ ██╔╝  ███████╗  ██╔████╔██║  ║
║                     ╚████╔╝   ╚════██║  ██║╚██╔╝██║  ║
║                      ╚██╔╝    ███████║  ██║ ╚═╝ ██║  ║
║                       ╚═╝     ╚══════╝  ╚═╝     ╚═╝  ║
║                     ** By Gabin Degrange - 2025 **   ║
╚══════════════════════════════════════════════════════╝
"""
        print(starting_screen)

    def close(self) -> None:
        """
        Ferme proprement le fichier de log.
        Il est recommandé d'appeler cette méthode en fin d'utilisation.
        """
        if self.log_file and not self.log_file.closed:
            self.log_file.close()


def main():
    """
    Fonction principale démontrant l'utilisation avancée de la classe Logger :
      1. Affichage de l'écran de démarrage.
      2. Création d'une instance Logger avec gestion des logs en fichier.
      3. Écriture et affichage des logs avec horodatage.
         Le fichier de log reçoit un niveau de messages supérieur (plus détaillé) que l'affichage.
      4. Démonstration de la barre de chargement en mode simulation classique,
         puis le suivi d'un phénomène réel avec affichage intégré de la durée.
      5. Fermeture propre du fichier de log.
    """
    # Afficher l'écran de démarrage
    Logger.show_starting_screen()

    # Instanciation du logger avec le niveau minimal pour l'affichage en console.
    # Par exemple, avec "INFO", la console affichera INFO et plus, alors que le fichier recevra DEBUG et plus.
    logger = Logger(level="INFO")

    # Exemples de logs
    logger.debug("Ceci est un message de DEBUG pour le suivi interne.")
    logger.info("Information utile pour l'utilisateur.")
    logger.warning("Attention : vérifiez les paramètres de configuration!")
    logger.error("Erreur critique détectée, veuillez intervenir immédiatement.")

    # Barre de chargement en mode simulation classique
    logger.info("Démarrage d'un processus simulé (mode classique)...")
    Logger.show_loading_bar(total=50, prefix="Chargement", suffix="Terminé", sleep_time=0.05, integrate=True)
    logger.info("Processus simulé terminé.")

    # Barre de chargement pour suivre un phénomène réel simulé.
    logger.info("Démarrage d'un phénomène réel simulé...")
    start_time = time.time()
    duration = 3  # durée du phénomène en secondes

    def progress_callback() -> float:
        # Calcule l'avancement en fonction du temps écoulé.
        return min((time.time() - start_time) / duration, 1.0)

    # La barre intégrée effacera la ligne une fois terminée et affichera le log avec la durée.
    Logger.show_loading_bar(prefix="Traitement", suffix="Terminé", sleep_time=0.1,
                            progress_callback=progress_callback, integrate=True, start_time=start_time)
    # Ici, le message de durée est affiché automatiquement par la méthode show_loading_bar.

    # Fermeture propre du logger
    logger.close()


if __name__ == '__main__':
    main()
