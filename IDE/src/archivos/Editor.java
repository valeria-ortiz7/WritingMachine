/** Instituto Tecnológico de Costa Rica
 *  Lenguajes, Compiladores e Interpretes
 *  Prof. Marco Hernandez Vasquez
 *  I Semestre, 2021
 *
 * @author Steven Badilla, Valeria Ortiz, Andrey Sanchez, Bryan Solano
 */

package archivos;

import java.io.IOException;

public class Editor {

    // Archivo que se esta creando o modificando en el IDLE
    private Documento archivo;

    /**
     * Constructor de la clase Editor
     */
    public Editor(){
        archivo = null;
    }

    /**
     * Funcion para abrir un txt existente en el editor
     * @param ubicacion: Ubicacion del archivo
     * @return texto: Contenido del txt
     * @throws Exception: Error a la hora de abrir el archivo
     */
    public String abrirArchivo(String ubicacion) throws Exception {
        String texto = "";
        archivo = new Documento(ubicacion);
        try{
            texto = archivo.getTexto();
        }
        catch (IOException e){
            throw new Exception("No fue posible cargar el archivo.", e);
        }
        return texto;
    }

    /**
     * Funcion para guardar un archivo nuevo o existente desde el editor
     * @param texto: Contenido del txt
     * @param ubicacion: Ubicacion del archivo
     * @throws Exception: Error a la hora de escribir el archivo
     */
    public void guardarArchivo(String texto, String ubicacion) throws Exception{
        if (archivo == null){
            archivo= new Documento(ubicacion);
        }
        try{
            archivo.guardar(texto);
        }
        catch (IOException e){
            throw new Exception("No fue posible guardar el archivo.", e);
        }
    }

    /**
     * Funcion para crear un nuevo txt desde el editor
     */
    public void crearArchivo(){
        archivo = null;
    }

    /**
     * Funcion para identificar si el archivo actual es nuevo o no
     * @return bool: True si el archivo es null, False en caso contrario
     */
    public boolean isNuevo(){
        return archivo == null;
    }

    /**
     * Funcion para retornar el nombre del archivo en caso de ya existir
     * @return archivo.getTxtPath(): String con el nombre de archivo
     */
    public String nombreTxt(){
        return archivo.getTxtPath();
    }
}
