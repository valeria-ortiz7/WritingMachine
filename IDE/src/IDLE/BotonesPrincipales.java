package IDLE;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class BotonesPrincipales extends JPanel implements ActionListener {

    public static final String CREAR = "CREAR";
    public static final String ABRIR = "ABRIR";
    public static final String GUARDAR = "GUARDAR";

    private JButton buttonAbrir;
    private JButton buttonCrear;
    private JButton buttonGuardar;
    private IDLE ventanaPrincipal;

    public BotonesPrincipales(IDLE ventanaPrincipal){
        this();
        this.ventanaPrincipal = ventanaPrincipal;
    }

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
    }


    @Override
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
    }
}
