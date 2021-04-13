/** Instituto Tecnológico de Costa Rica
 *  Lenguajes, Compiladores e Interpretes
 *  Prof. Marco Hernandez Vasquez
 *  I Semestre, 2021
 *
 * @author Steven Badilla, Valeria Ortiz, Andrey Sanchez, Bryan Solano
 */

package IDLE;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.IOException;

public class BotonesPrincipales extends JPanel implements ActionListener {

    // Comandos de accion para los botones
    public static final String CREAR = "CREAR";
    public static final String ABRIR = "ABRIR";
    public static final String GUARDAR = "GUARDAR";
    public static final String COMPILAR = "COMPILAR";
    public static final String EJECUTAR = "EJECUTAR";

    // Definicion de los botones de interfaz
    private JButton buttonAbrir;
    private JButton buttonCrear;
    private JButton buttonGuardar;
    private JButton buttonCompilar;
    private JButton buttonEjecutar;

    // Inclusion del JFrame, debido a ser componentes activos en el
    private IDLE ventanaPrincipal;

    /**
     * Constructor llamado en el IDLE para activarlo como panel activo
     * @param ventanaPrincipal: JFrame donde se va a utilizar el panel
     */
    public BotonesPrincipales(IDLE ventanaPrincipal){
        this();
        this.ventanaPrincipal = ventanaPrincipal;
    }

    /**
     * Constructor del JPanel y todos sus componentes
     */
    public BotonesPrincipales(){
        setLayout(new GridLayout(1,0,2,0));

        buttonAbrir = new JButton("Abrir Archivo");
        buttonAbrir.setActionCommand(ABRIR);
        buttonAbrir.addActionListener(this);
        add(buttonAbrir);

        buttonCrear = new JButton("Crear Archivo");
        buttonCrear.setActionCommand(CREAR);
        buttonCrear.addActionListener(this);
        add(buttonCrear);

        buttonGuardar = new JButton("Guardar Archivo");
        buttonGuardar.setActionCommand(GUARDAR);
        buttonGuardar.addActionListener(this);
        add(buttonGuardar);

        buttonCompilar = new JButton("Compilar");
        buttonCompilar.setActionCommand(COMPILAR);
        buttonCompilar.addActionListener(this);
        add(buttonCompilar);

        buttonEjecutar = new JButton("Ejecutar");
        buttonEjecutar.setActionCommand(EJECUTAR);
        buttonEjecutar.addActionListener(this);
        add(buttonEjecutar);
    }


    @Override
    /**
     * Sobreescritura del metodo actionPerformed para asignar
     * las acciones correspondientes a cada boton
     */
    public void actionPerformed(ActionEvent actionEvent) {
        if(actionEvent.getActionCommand().equals(ABRIR)){
            ventanaPrincipal.abrirTXT();
        }
        else if(actionEvent.getActionCommand().equals(CREAR)){
            ventanaPrincipal.crearTXT();
        }
        else if(actionEvent.getActionCommand().equals(GUARDAR)){
            ventanaPrincipal.guardarTXT();
        }
        else if(actionEvent.getActionCommand().equals(COMPILAR)){
            ventanaPrincipal.compilar();

        }
        else if(actionEvent.getActionCommand().equals(EJECUTAR)){
            ventanaPrincipal.ejecutar();
        }
    }
}
