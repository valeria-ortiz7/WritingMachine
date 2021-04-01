package IDLE;

import archivos.Editor;

import javax.swing.*;
import javax.swing.border.EmptyBorder;
import java.awt.*;
import java.io.File;

public class IDLE extends JFrame {

    private JPanel contentPane;
    private BotonesPrincipales botonesPrincipales;
    private TextEditor textEditor;

    private Editor editor;

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

    public IDLE(){
        editor = new Editor();
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setBounds(100,100,450,300);
        contentPane = new JPanel();
        contentPane.setBorder(new EmptyBorder(5,5,5,5));
        contentPane.setLayout(new BorderLayout(0,0));
        setContentPane(contentPane);

        botonesPrincipales = new BotonesPrincipales(this);
        contentPane.add(botonesPrincipales, BorderLayout.NORTH);

        textEditor = new TextEditor();
        contentPane.add(textEditor, BorderLayout.CENTER);
    }

    public void abrirTXT(){
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

    public void crearTXT(){
        editor.crearArchivo();
        textEditor.refresh("");
    }

    public void guardarTXT(){
        String ruta = "";
        String contenido = "";
        if(editor.isNuevo()){
            JFileChooser fc = new JFileChooser();
            if(fc.showSaveDialog(this) == JFileChooser.APPROVE_OPTION){
                ruta = fc.getSelectedFile().getAbsolutePath();
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
    }
}
