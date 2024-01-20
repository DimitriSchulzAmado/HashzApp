import flet as ft

def main(page):
    page.title = "Hashzapp"
    
    title = ft.Text("Hashzapp", size=30, color=ft.colors.BLUE_500, )
    username = ft.TextField(label="Escreva seu nome")
    
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    chat = ft.Column()
    
    
    def tunel_send_message(message):
        """Manage the tunel communication between users"""
        type_message = message["type"]
        if type_message == "message":
            text_message = message["text"]
            user_message = message["user"]
            # Add the message to chat
            chat.controls.append(ft.Text(f"{user_message}: {text_message}"))
        else:
            user_message = message["user"]
            chat.controls.append(ft.Text(f"{user_message} entrou no chat",
                                         size=12, italic=True, color=ft.colors.GREEN_500))
        page.update()
    
    page.pubsub.subscribe(tunel_send_message)
    
    def send_message(e):
        """Send message to chat"""
        if message_field.value == "":
            return
        else:
            page.pubsub.send_all({"text": message_field.value, "user": username.value,
                                    "type": "message"})
            # colocar o nome do usuario na mensagem
            message = f'{username.value}: {message_field.value}'
            
            page.pubsub.send_all(message) # Envia a mensagem para todos os usuarios
            
            # Limpar o campo da mensagem
            message_field.value = ""
            page.update()
        
    message_field = ft.TextField(label="Escreva sua mensagem",
                                 on_submit=send_message)
    
    send_button = ft.IconButton(icon="send", on_click=send_message)
    
    def enter_popup(e):
        """Open chat"""
        page.pubsub.send_all({"user": username.value, "type": "entrada"})
        # Adiciona o chat
        page.add(chat)
        # Fecha o popup
        popup.open = False
        # Remove o botão de iniciar chat
        page.remove(start_button)
        page.remove(title)
        # Cria o campo e o botão de enviar mensagens
        page.add(message_field)
        page.add(send_button)
        message_row = ft.Row(
            [
                message_field,
                send_button
            ],
            alignment=ft.MainAxisAlignment.END
        )
        page.update()
    
    popup = ft.AlertDialog(
        open=False,
        modal=True,
        title=ft.Text("Bem vindo ao Hashzapp"),
        content=username,
        actions=[ft.ElevatedButton(text="Entrar", on_click=enter_popup)]
    )
    
    def enter_chat(e):
        page.dialog = popup
        popup.open = True
        page.update()
    
    start_button = ft.ElevatedButton(text="Iniciar Chat", on_click=enter_chat)
    
    page.add(title)
    page.add(start_button)
    

#ft.app(target=main)
ft.app(target=main, view=ft.WEB_BROWSER) # Para abrir no navegador