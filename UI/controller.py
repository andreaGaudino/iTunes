import warnings

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, e):
        try:
            totDint = int(self._view.txtInDurata.value)
        except ValueError:
            warnings.warn_explicit(message="Durata non intera", category=TypeError, filename="controller.py", lineno=15)
            return


        self._model.buildGraph(totDint)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato"))
        nN, nE = self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {nN} nodi e {nE} archi"))




        nodes = self._model.getNodes()
        nodes.sort(key = lambda x: x.Title)
        # for n in nodes:
        #     self._view.ddAlbum.options.append(
        #         ft.dropdown.Option(data=n,
        #                            text=n.Title,
        #                            on_click=self.getSelectedAlbum
        #                            )
        #                         )
        #
        listDD = map(lambda x: ft.dropdown.Option(data=x,
                                   text=x.Title,
                                   on_click=self.getSelectedAlbum
                                   ), nodes )
        self._view.ddAlbum.options = listDD

        self._view.update_page()



    def getSelectedAlbum(self, e):
        if e.control.data is None:
            self.choiceAlbum = None
        else:
            self.choiceAlbum = e.control.data
        print(self.choiceAlbum)


    def handleAnalisiComp(self, e):
        if self.choiceAlbum is None:
            warnings.warn("Album non selezionato")
            return
        sizeC, totD = self._model.getConnessaDetails(self.choiceAlbum)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"La componente connessa che include {self.choiceAlbum}"
                                                      f" ha dimensione {sizeC} e ha durata complessiva = {totD}"))
        self._view.update_page()


    def handleGetSetAlbum(self, e):
        a1 = self.choiceAlbum
        dTOTtxt = self._view.txtInSoglia.value
        try:
            dTOT = int(dTOTtxt)
        except ValueError:
            warnings.warn("Soglia not integer")
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Soglia inserita non valida"))
            return

        if a1 is None:
            warnings.warn("Attenzione, album non selezionato")
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Album non selezionato"))
            return

        setAlbum, durata = self._model.getSetAlbum(a1, dTOT)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Set album ottimo trovato con durata: {durata}"))
        for s in setAlbum:
            self._view.txt_result.controls.append(ft.Text(f"{s}"))

        self._view.update_page()