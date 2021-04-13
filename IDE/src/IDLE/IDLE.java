/** Instituto Tecnológico de Costa Rica
 *  Lenguajes, Compiladores e Interpretes
 *  Prof. Marco Hernandez Vasquez
 *  I Semestre, 2021
 *
 * @author Steven Badilla, Valeria Ortiz, Andrey Sanchez, Bryan Solano
 */

package IDLE;

import archivos.*;

import javax.swing.*;
import javax.swing.border.EmptyBorder;
import javax.swing.filechooser.FileNameExtensionFilter;
import java.awt.*;
import java.io.File;
import java.io.IOException;

public class IDLE extends JFrame {

    // Definicion del Panel contenedor de los demas paneles
    private JPanel contentPane;

    // Definicion de los paneles a agregar
    private BotonesPrincipales botonesPrincipales;
    private TextEditor textEditor;
    private CompilerLog compilerLog;


    // Definicion del objeto editor que maneja el txt
    private Editor editor;

    private Documento eventlog;

    private String dir = System.getProperty("user.dir");

    /**
     * Main que crea el JFrame y sus componentes graficos
     * @param args
     */
    public static void main(String[] args){
        EventQueue.invokeLater(new Runnable() {
            @Override
            public void run() {
                try{
                    IDLE frame = new IDLE();
                    frame.setVisible(true);
                }
                catch (Exception e){
                    e.printStackTrace();
                }
            }
        });

    }

    /**
     * Constructor del JFrame y sus componentes
     */
    public IDLE(){
        editor = new Editor();
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setBounds(200,50,900,700);
        contentPane = new JPanel();
        contentPane.setBorder(new EmptyBorder(5,5,5,5));
        contentPane.setLayout(new BorderLayout(0,0));
        contentPane.setBackground(new Color(50, 56, 66));
        setContentPane(contentPane);

        botonesPrincipales = new BotonesPrincipales(this);
        contentPane.add(botonesPrincipales, BorderLayout.NORTH);

        textEditor = new TextEditor();
        contentPane.add(textEditor, BorderLayout.CENTER);

        compilerLog = new CompilerLog();
        compilerLog.setPreferredSize(new Dimension(600,100));
        contentPane.add(compilerLog, BorderLayout.SOUTH);

        this.setTitle("Writting Machine - Documento sin guardar");
        eventlog = new Documento(dir + "/Compilador/error.txt");

    }

    /**
     * Funcion que comunica el manejo de la informacion del txt con la seleccion
     * basica de archivos en la interfaz para abrir un txt existente
     */
    public void abrirTXT(){
        if(editor.isNuevo() && textEditor.getTexto().equals("")){
            JFileChooser fc = new JFileChooser();
            FileNameExtensionFilter filter = new FileNameExtensionFilter("TEXT FILES", "txt", "text");
            fc.setFileFilter(filter);
            if(fc.showOpenDialog(this) == JFileChooser.APPROVE_OPTION){
                File f = fc.getSelectedFile();
                String contenido = "";
                try{
                    contenido = editor.abrirArchivo(f.getAbsolutePath());
                    textEditor.refresh(contenido);
                }
                catch (Exception e){
                    JOptionPane.showMessageDialog(this,e.getMessage(),"IDLE",JOptionPane.ERROR_MESSAGE);
                }
            }
        }
        else {
            int reply = JOptionPane.showConfirmDialog(this, "Desea guardar el archivo?", "IDLE", JOptionPane.YES_NO_OPTION);
            if (reply == JOptionPane.YES_OPTION) {
                guardarTXT();
            }
            JFileChooser fc = new JFileChooser();
            if(fc.showOpenDialog(this) == JFileChooser.APPROVE_OPTION){
                File f = fc.getSelectedFile();
                String contenido = "";
                try{
                    contenido = editor.abrirArchivo(f.getAbsolutePath());
                    textEditor.refresh(contenido);
                }
                catch (Exception e){
                    JOptionPane.showMessageDialog(this,e.getMessage(),"IDLE",JOptionPane.ERROR_MESSAGE);
                }
            }
        }
        String path = editor.nombreTxt().substring(editor.nombreTxt().lastIndexOf('/') + 1);
        this.setTitle("Writting Machine - " + path);

    }

    /**
     * Funcion que comunica el manejo de la informacion del txt con la seleccion
     * basica de archivos en la interfaz para crear un nuevo txt
     */
    public void crearTXT(){
        if(editor.isNuevo() && textEditor.getTexto().equals("")){
            editor.crearArchivo();
            this.setTitle("Writting Machine - Documento sin guardar");
            textEditor.refresh("");
        }
        else {
            int reply = JOptionPane.showConfirmDialog(this, "Desea guardar el archivo?", "IDLE", JOptionPane.YES_NO_OPTION);
            if (reply == JOptionPane.YES_OPTION) {
                guardarTXT();
            }
            editor.crearArchivo();
            this.setTitle("Writting Machine - Documento sin guardar");
            textEditor.refresh("");

        }

    }

    /**
     * Funcion que comunica el manejo de la informacion del txt con la seleccion
     * basica de archivos en la interfaz para guardar un txt nuevo o existente
     */

    public void guardarTXT(){
        String ruta = "";
        String contenido = "";
        if(editor.isNuevo()){
            JFileChooser fc = new JFileChooser();
            if(fc.showSaveDialog(this) == JFileChooser.APPROVE_OPTION){
                ruta = fc.getSelectedFile().getAbsolutePath()+".txt";
            }
        }
        contenido = textEditor.getTexto();
        try{
            editor.guardarArchivo(contenido,ruta);
            JOptionPane.showMessageDialog(this,"Archivo guardado con éxito!","IDLE",JOptionPane.INFORMATION_MESSAGE);
        }
        catch (Exception e){
            JOptionPane.showMessageDialog(this,e.getMessage(),"IDLE",JOptionPane.ERROR_MESSAGE);
        }
        String path = editor.nombreTxt().substring(editor.nombreTxt().lastIndexOf('/') + 1);
        this.setTitle("Writting Machine - " + path);
    }

    /**
     * Funcion que comunica el manejo de la informacion del txt con el compilador
     * de python para compilar el archivo actual
     */
    public void compilar(){
        guardarTXT();
        // Se inicializa el proceso de compilacion
        try{
            compilerLog.setTextColor(0);
            compilerLog.refresh("Iniciando el proceso de compilacion...");
            Thread.sleep(1000);

            Process process = Runtime.getRuntime().exec("python3 " + dir + "/Compilador/compilador.py "  + editor.nombreTxt());
            process.waitFor();
            if(eventlog.getTexto().equals("")){
                compilerLog.setTextColor(2);
            }
            else{
                compilerLog.setTextColor(1);
            }
            compilerLog.refresh(eventlog.getTexto() + "\n" + "Compilacion finalizada");

        }
        catch (Exception e){
            JOptionPane.showMessageDialog(this,e.getMessage(),"IDLE",JOptionPane.ERROR_MESSAGE);
        }
    }

    /**
     * Funcion que comunica el manejo de la informacion del txt con el compilador
     * de python para compilar y ejecutar el archivo actual
     */
    public void ejecutar(){
        guardarTXT();
        // Se inicializa el proceso de compilacion
        try{
            compilerLog.setTextColor(0);
            compilerLog.refresh("Iniciando el proceso de compilacion...");
            Thread.sleep(1000);
            
            Process process = Runtime.getRuntime().exec("python3 " + dir + "/Compilador/ejecutar.py "  + editor.nombreTxt());
            process.waitFor();
            if(eventlog.getTexto().equals("")){
                compilerLog.setTextColor(2);
            }
            else{
                compilerLog.setTextColor(1);
            }
            compilerLog.refresh(eventlog.getTexto() + "\n" + "Compilacion finalizada");

        }
        catch (Exception e){
            JOptionPane.showMessageDialog(this,e.getMessage(),"IDLE",JOptionPane.ERROR_MESSAGE);
        }
    }

}
