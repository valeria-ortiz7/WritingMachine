package IDLE;

import javax.swing.*;
import java.awt.*;

public class TextEditor extends JPanel {

    private JPanel panel1;
    private JTextArea taEditor;
    private JScrollPane scrollpane;

    public TextEditor(){
        setLayout(new BorderLayout(0,0));

        scrollpane = new JScrollPane();
        add(scrollpane, BorderLayout.CENTER);

        taEditor = new JTextArea();
        scrollpane.setViewportView(taEditor);

    }

    public String getTexto(){
        return taEditor.getText();
    }

    public void refresh(String texto){
        taEditor.setText(texto);
    }
}
