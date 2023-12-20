import time
import random

# Grafo klasė
class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = []

    # Kraštinės pridėjimas
    def addEdge(self, u, v, w):
        self.graph.append([u, v, w])

    # Funkcija, nustatyti elementui priklausančias viršūnes
    def find(self, parent, i):
        if parent[i] != i:
            # Path compression vykdymas
            parent[i] = self.find(parent, parent[i])
        return parent[i]

    # Funkcija, sujungianti medžius (pagal rangą)
    def union(self, parent, rank, x, y):
        if rank[x] < rank[y]:
            parent[x] = y
        elif rank[x] > rank[y]:
            parent[y] = x

        else:
            parent[y] = x
            rank[x] += 1

    # Kruskalo algoritmas
    def KruskalMST(self):
        result = []
        i = 0
        e = 0

        # Kraštinės išrikiuojamos pagal svorį ir viršūnės nr didėjimo tvarka
        self.graph = sorted(self.graph, key=lambda item: (item[2], item[0], item[1]))

        parent = []
        rank = []

        # Iniciuojami medžiai kiekvienai viršūnei
        for node in range(self.V):
            parent.append(node)
            rank.append(0)

        mst_output = "Kruskalo algoritmas\n"
        mst_output += "Kraštinės, sudarančios MAM:\n"

        # Galutinins kraštinių skaičius V-1
        while e < self.V - 1:
            
            u, v, w = self.graph[i]
            i = i + 1
            x = self.find(parent, u)
            y = self.find(parent, v)

            
            # Jei įtraukiant šią kraštinę nesusidaro ciklas, tada įtraukti ją į rezultatą
            # ir padidinti rezultato indeksą kitam kraštui
            if x != y:
                e = e + 1
                result.append([u, v, w])
                self.union(parent, rank, x, y)

        minimumCost = 0
        print("\nKruskalo algoritmas")
        for u, v, w in result:
            minimumCost += w
            mst_output += "%d -- %d == %d\n" % (u, v, w)
        mst_output += "MAM svoris: " + str(minimumCost) + "\n"

        return mst_output

    # Boruvkos algoritmas
    def boruvkaMST(self):
        parent = []; rank = []; 
        cheapest =[] # Saugoma 'pigiausios' kraštinės informacija
        numTrees = self.V # Pradinių medžių skaičius
        MSTweight = 0
        mst_output = "Boruvkos algoritmas\n"

        print("\nBoruvkos algoritmas")

        # Sukurti V medžius su vienu elementu
        for node in range(self.V):
            parent.append(node)
            rank.append(0)
            cheapest =[-1] * self.V

        # Veiksmai kartojami, kol lieka tik vienas medis
        while numTrees > 1:

            # Pereiti per visus kraštus ir atnaujinti pigiausią kiekvienos dalies kraštą
            for i in range(len(self.graph)):

                # Surasti komponentus dviejų dabartinio krašto kampų
                u,v,w = self.graph[i]
                set1 = self.find(parent, u)
                set2 = self.find(parent ,v)

            
                # Tikriname ar briauna nepriklauso dabariniam medžiui
                if set1 != set2:	 

                    if cheapest[set1] == -1 or cheapest[set1][2] > w :
                        cheapest[set1] = [u,v,w] 

                    if cheapest[set2] == -1 or cheapest[set2][2] > w :
                        cheapest[set2] = [u,v,w]

            for node in range(self.V):

                # Patikrinti, ar egzistuoja pigiausia dabartininio medžio briauna
                if cheapest[node] != -1:
                    u,v,w = cheapest[node]
                    set1 = self.find(parent, u)
                    set2 = self.find(parent ,v)

                    if set1 != set2 :
                        MSTweight += w
                        self.union(parent, rank, set1, set2)
                        mst_output += "%d -- %d == %d\n" % (u, v, w)
                        numTrees = numTrees - 1

            # Atsatatyti pigiausios kraštinės masyvą
            cheapest =[-1] * self.V

        mst_output += "MAM svoris %d\n" % MSTweight

        return mst_output


def generate_random_matrix(n, num_edges, max_weight):
    if num_edges < n - 1 or num_edges > (n * (n - 1)) // 2:
        raise ValueError("Negalimas briaunų skaičius grafui su {} viršūnėmis.".format(n))

    edges = set()
    # Sukuriamas karkasas
    for i in range(1, n):
        u = random.randint(0, i - 1)
        weight = random.randint(1, max_weight)
        edges.add((min(u, i), max(u, i), weight))

    # Pridedamos papildomos kraštinės
    while len(edges) < num_edges:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        weight = random.randint(1, max_weight)
        if u != v:
            edges.add((min(u, v), max(u, v), weight))

    # Sukuriama matrica
    matrix = [[0 for _ in range(n)] for _ in range(n)]
    for u, v, weight in edges:
        matrix[u][v] = matrix[v][u] = weight

    return matrix

def is_symmetric(matrix, n):
    for i in range(n):
        for j in range(n):
            if matrix[i][j] != matrix[j][i]:
                return False
    return True

def main():
    n = int(input("Įveskite grafo viršūnių skaičių: "))
    method = input(
        """Pasirinkite poragramos veikimo metodą: \n
        m -  kad įvestumėte duomenis;
        auto -  automatinei duomenų generacijai: \n"""
    )

    if method.lower() == "m":
        print("Įveskite grafo matricą eilutė po eilutės (naudokite 0, jei briaunos nėra):")

        matrix = []
        for i in range(n):
            row = list(map(int, input().split()))
            if len(row) != n:
                print("Eilutėje turi būti ", n, "elementų. Pabandykite darkart.")
                return
            matrix.append(row)

        if not is_symmetric(matrix, n):
            print("Matrica yra nesimetriška. Prašome įvesite simetrišką matricą, reprezentuojančia norimą grafą.")
            return


    elif method.lower() == "auto":
        max_weight = 100
        num_edges = int(input("Įveskite briaunų skaičių: "))

        try:
            matrix = generate_random_matrix(n, num_edges, max_weight)
        except ValueError as e:
            print(e)
            return
        print("Sugeneruota grafo matrica faile matrix.txt")
        with open("matrix.txt", "w") as file:
            for row in matrix:
                file.write(" ".join(map(str, row)) + "\n")

    else:
        print("Įvestis neteisnga.")
        return

    g = Graph(n)
    for i in range(n):
        for j in range(i + 1, n):
            if matrix[i][j] != 0:  # 0 reiškia kraštinės nebuvimą
                g.addEdge(i, j, matrix[i][j])

    start_time = time.perf_counter()
    boruvka_output = g.boruvkaMST()
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print("Programos trukmė (Boruvkos algoritmas) ", round(elapsed_time, 5), "s")
    print("Boruvkos algoritmo MAM ir svorį rasite faile boruvka_output.txt")
    
    start_time = time.perf_counter()
    kruskal_output = g.KruskalMST()
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print("Programos trukmė (Kruskalo algoritmas) ", round(elapsed_time, 5), "s")
    print("Kruskalo algoritmo MAM ir svorį rasite faile kruskals_output.txt")

    # Kruskalo išvestis į failą
    with open("kruskal_output.txt", "w") as file:
        file.write(kruskal_output)

    # Boruvkos išvestis į failą
    with open("boruvka_output.txt", "w") as file:
        file.write(boruvka_output)   

if __name__ == "__main__":
    main()