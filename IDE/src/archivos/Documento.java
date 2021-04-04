/** Instituto Tecnológico de Costa Rica
 *  Lenguajes, Compiladores e Interpretes
 *  Prof. Marco Hernandez Vasquez
 *  I Semestre, 2021
 *
 * @author Steven Badilla, Valeria Ortiz, Andrey Sanchez, Bryan Solano
 */

package archivos;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;

public class Documento {

    /**
     * Archivo en la computadora
     */
    private File txt;

    /**
     * Constructor de la clase Documento
     * @param nombre: Ruta del archivo
     */
    public Documento(String nombre){
        txt = new File(nombre);

    }

    /**
     * Funcion para obtener el texto de un txt
     * @return texto: String con el contenido del txt
     * @throws IOException: Error a la hora de abrir el txt
     */
    public String getTexto() throws IOException {
        String texto = "";
        FileReader fr = new FileReader(txt);
        BufferedReader br = new BufferedReader(fr);
        String lineaActual = br.readLine();
        while (lineaActual != null) {
            texto += lineaActual + "\n";
            lineaActual = br.readLine();
        }
        br.close();
        fr.close();
        return texto;
    }

    /**
     * Funcion para guardar contenido en un txt
     * @param texto: String con el contenido a guardar
     * @throws IOException: Error a la hora de guardar el txt
     */
    public void guardar(String texto) throws IOException{
        PrintWriter pw = new PrintWriter(txt);
        pw.write(texto);
        pw.close();
    }

}
