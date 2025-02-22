from process import Process 
from factory_process import Facory_Process
import graphviz  # Assurez-vous que la bibliothèque graphviz est installée

class vsm:
    def __init__(self):
        self.process_list: list[Process] = []
        # Stocke les liaisons sous forme de tuples (parent, child)
        self.links: list[tuple[Process, Process]] = []
        
    def add_process(self, process: Process):
        self.process_list.append(process)
        
    def link_processes(self, parent: Process, child: Process) -> None:
        if parent not in self.process_list or child not in self.process_list:
            print("Les deux process doivent être ajoutés avant de créer un lien.")
        else:
            self.links.append((parent, child))
            
    def get_dot(self) -> str:
        # Génération d'un graph complet sous forme de chaîne au format DOT.
        # 'rankdir=LR' indique une orientation de gauche à droite.
        dot = "digraph ProcessGraph {\n"
        dot += "    rankdir=LR;\n"
        dot += "    node [style=filled, fillcolor=lightblue];\n"
        # Ajoute tous les noeuds avec une forme spécifique selon le type.
        for process in self.process_list:
            if isinstance(process, Facory_Process):
                shape = "triangle"
            else:
                shape = "box"
            dot += f'    "{process.get_name()}" [label="{process.get_name()}", shape={shape}];\n'
        # Ajoute les liaisons (arêtes)
        for parent, child in self.links:
            dot += f'    "{parent.get_name()}" -> "{child.get_name()}";\n'
        dot += "}\n"
        return dot

    def show_graph(self) -> None:
        """Génère et affiche le graphe en utilisant Graphviz."""
        dot_str = self.get_dot()
        graph = graphviz.Source(dot_str)
        graph.render('process_graph', view=True, format='png')
        
    def __repr__(self):
        return self.get_dot()
        
if __name__ == "__main__":
    vsm_instance = vsm()
    
    # Création de plusieurs process
    proc1 = Facory_Process(name="Process1", process_time=10, time_variability=2, quality=5)
    proc2 = Process(name="Process2")
    proc3 = Process(name="Process3")
    proc4 = Process(name="Process4")
    proc5 = Process(name="Process5")
    proc6 = Process(name="Process6")
    
    vsm_instance.add_process(proc1)
    vsm_instance.add_process(proc2)
    vsm_instance.add_process(proc3)
    vsm_instance.add_process(proc4)
    vsm_instance.add_process(proc5)
    vsm_instance.add_process(proc6)
    
    # Création de liens illustrant une structure mixte
    vsm_instance.link_processes(proc1, proc2)
    vsm_instance.link_processes(proc1, proc3)
    vsm_instance.link_processes(proc1, proc6)
    vsm_instance.link_processes(proc2, proc4)
    vsm_instance.link_processes(proc3, proc4)
    vsm_instance.link_processes(proc6, proc5)
    vsm_instance.link_processes(proc4, proc5)
    
    # Affiche le DOT dans la console
    print(vsm_instance)
    # Affiche la visualisation graphique (génère un fichier process_graph.png et l'ouvre)
    vsm_instance.show_graph()
