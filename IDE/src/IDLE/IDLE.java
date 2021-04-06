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
        setBounds(100,100,600,500);
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

        eventlog = new Documento("/home/andreyzarttys/Documentos/TEC/VII Semestre/Compi/WritingMachine/IDE/errorLog.txt");
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



        try{
            compilerLog.refresh(eventlog.getTexto());
        }
        catch (Exception e){
            JOptionPane.showMessageDialog(this,e.getMessage(),"IDLE",JOptionPane.ERROR_MESSAGE);
        }
    }

    public void compilar(){
        // Se inicializa el proceso de compilacion
        try{
            compilerLog.refresh(eventlog.getTexto());
            Process process = Runtime.getRuntime().exec("python3 /home/andreyzarttys/Documentos/TEC/VII Semestre/Compi/WritingMachine/parser.py " + editor.nombreTxt());
        }
        catch (Exception e){
            JOptionPane.showMessageDialog(this,e.getMessage(),"IDLE",JOptionPane.ERROR_MESSAGE);
        }

        // Se refresca con los resultados y se deja listo para la proxima compilacion
        try{
            compilerLog.refresh(eventlog.getTexto());
            eventlog.guardar("Iniciando el proceso de compilacion...");
        }
        catch (Exception e){
            JOptionPane.showMessageDialog(this,e.getMessage(),"IDLE",JOptionPane.ERROR_MESSAGE);
        }
    }
}
