from django.shortcuts import render
from rest_framework import viewsets , generics
from .models import User, UserSkills, Topic, Level, Question, WeeklyChallenge, Score, UserProfile,PontuationUserLevel,Comunidade,UserComunity,UserTopicInterest
from .serializer import UserSerializer, UserSkillsSerializer, TopicSerializer, LevelSerializer, QuestionSerializer, WeeklyChallengeSerializer, ScoreSerializer, AudioJsonSerializer,ComunidadeSerializer,UserComunitySerializer,UserTopicInterestSerializer, PontuationUserLevelSerializer
from .serializer import UserContextSerializer
from .models import UserContext
import base64
from pydub import AudioSegment
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from google.cloud import speech_v1p1beta1 as speech
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import openai
from django.conf import settings
from django.http import JsonResponse
from groq import Groq
from django.core.files.storage import default_storage
from difflib import SequenceMatcher
import os

# Configurar el cliente de OpenAI
openai.api_key = settings.API_KEY_OPENAI

# Configurar el cliente de GROQ
groq_client = Groq(
    api_key=settings.API_KEY_GROQ,
)


# Create your views here.
@api_view(["POST"])
def logout_user(request):
    if request.method == "POST":
        request.user.auth_token.delete()
        return Response({"Message": "You are logget out"}, status = status.HTTP_200) 



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserSkillsViewSet(viewsets.ModelViewSet):
    queryset = UserSkills.objects.all()
    serializer_class = UserSkillsSerializer

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

class LevelViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class WeeklyChallengeViewSet(viewsets.ModelViewSet):
    queryset = WeeklyChallenge.objects.all()
    serializer_class = WeeklyChallengeSerializer

class PontuationUserLevelViewSet(viewsets.ModelViewSet):
    queryset = PontuationUserLevel.objects.all()
    serializer_class = PontuationUserLevelSerializer

class UserTopicInterestViewSet(viewsets.ModelViewSet):
    queryset = UserTopicInterest.objects.all()
    serializer_class = UserTopicInterestSerializer

class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer

class ComunidadeViewSet(viewsets.ModelViewSet):
    queryset = Comunidade.objects.all()
    serializer_class = ComunidadeSerializer

class UserComunityViewSet(viewsets.ModelViewSet):
    queryset = UserComunity.objects.all()
    serializer_class = UserComunitySerializer

class UserContextViewSet(viewsets.ModelViewSet):
    queryset = UserContext.objects.all()
    serializer_class = UserContextSerializer

class AudioUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = AudioJsonSerializer(data=request.data)
        if serializer.is_valid():
            audio_data = serializer.validated_data
            audio_bytes = base64.b64decode(audio_data['audio_bytes'])
            
            client = speech.SpeechClient()
            audio = speech.RecognitionAudio(content=audio_bytes)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=audio_data['frame_rate'],
                language_code='pt-BR',
            )
            response = client.recognize(config=config, audio=audio)
            
            transcript = ""
            for result in response.results:
                transcript += result.alternatives[0].transcript + " "
            
            return Response({"transcript": transcript.strip()}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET']) 
def get_user_profile(request):
    user = request.user
    try:
        user_profile = UserProfile.objects.get(user=user)
        user_info = User.objects.get(id=user.id)

        user_data = {
            'name': user_info.full_name,
            'username': user_info.username,
            'nacionalidade': user_profile.idioma_estudiado,
            'streak': user_profile.streak,
            'goal': user_profile.objetivo,
            'image_profile': user_profile.profile_pic,  # Se profile_pic for uma ImageField, adicione .url
            'progress': user_profile.progress
        }
        return Response(user_data, status=status.HTTP_202_ACCEPTED)
    except UserProfile.DoesNotExist:
        return Response({'error': 'User profile not found'}, status=404)



@api_view(['GET'])
def return_id(request):
    user_id = request.user.id
    return Response(user_id)
# Vista para obtener preguntas por nivel y tipo
@api_view(['GET'])
def get_questions(request, id_level, q_type):
    questions = Question.objects.filter(level=id_level, type=q_type)
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)

# Vista para obtener niveles por tópico
@api_view(['GET'])
def get_levels(request, id_topic):
    levels = Level.objects.filter(topic=id_topic)
    serializer = LevelSerializer(levels, many=True)
    return Response(serializer.data)

# Vista para obtener retos semanales filtrados por fecha
@api_view(['GET'])
def get_weekly_challenge(request, id_topic, start_date, end_date):
    challenges = WeeklyChallenge.objects.filter(topic=id_topic, start_date__gte=start_date, end_date__lte=end_date)
    serializer = WeeklyChallengeSerializer(challenges, many=True)
    return Response(serializer.data)

# Vista para obtener score y status por usuario y reto
@api_view(['GET'])
def get_user_score(request, id_user, id_challenge):
    score = Score.objects.filter(user=id_user, challenge=id_challenge).first()
    serializer = ScoreSerializer(score)
    return Response(serializer.data)

# Vista para obtener puntuación del usuario en un nivel
@api_view(['GET'])
def get_user_pontuation(request, user_id, id_topic, id_level):
    pontuation = PontuationUserLevel.objects.filter(user=user_id, level__topic=id_topic, level=id_level).first()
    serializer = PontuationUserLevel(pontuation)
    return Response(serializer.data)

# Vista para actualizar puntuación
@api_view(['POST'])
def load_pontuation(request):
    user_id = request.data.get('id_user')
    topic_id = request.data.get('topic')
    level_id = request.data.get('level')
    pontuation = request.data.get('pontuation')
    
    try:
        pontuation_record = PontuationUserLevel.objects.get(user=user_id, level=level_id)
        if pontuation > 0 and pontuation > pontuation_record.pontuation:
            pontuation_record.pontuation = pontuation
            pontuation_record.save()
            return Response({'status': 'updated'})
    except PontuationUserLevel.DoesNotExist:
        if pontuation > 0:
            new_record = PontuationUserLevel(user_id=user_id, level_id=level_id, pontuation=pontuation)
            new_record.save()
            return Response({'status': 'created'})
    
    return Response({'status': 'failed'}, status=400)

# Crearmos un path que te devuelve el contexto
@api_view(['GET'])
def get_user_context(request, user_id,chat_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': f'El usuario {user_id} no existe'}, status=400)

    user_context, created = UserContext.objects.get_or_create(user=user)

    if user_context :
        if user_context.context_data :
            # Buscar el chat_id en el contexto existente
            chat = next((chat for chat in user_context.context_data if chat['chat_id'] == chat_id), None)

            if chat:
                return JsonResponse({'context': chat['data']})
            else:
                return JsonResponse({'error': 'No se ha encontrado el chat_id en el contexto del usuario'}, status=404)
            
        else:
            return JsonResponse({'error': 'El contexto del usuario no contiene la clave "data"'}, status=404)
    else:
        return JsonResponse({'error': 'No se ha encontrado el contexto del usuario'}, status=404)

# Creamos un path que te devuelve el contexto del usuario por id
@api_view(['GET'])
def get_all_chats_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': f'El usuario {user_id} no existe'}, status=400)

    user_context, created = UserContext.objects.get_or_create(user=user)

    if user_context :
        if user_context.context_data :
            return JsonResponse({'context': user_context.context_data})
        else:
            return JsonResponse({'error': 'El contexto del usuario no contiene la clave "data"'}, status=404)
    else:
        return JsonResponse({'error': 'No se ha encontrado el contexto del usuario'}, status=404)
 

# Vista para chatbot
@api_view(['POST'])
def pathLLM_chatbot(request):
    user_id = request.data.get('user_id')
    prompt = request.data.get('prompt')
    personalidad = request.data.get('personalidad')
    provider = request.data.get('provider')
    chat_id = request.data.get('chat_id')
    model = request.data.get('model')

    # Verificar si el usuario existe en la base de datos
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': f'El usuario {user_id} no existe'}, status=400)

    # Verificar si el usuario tiene un UserContext
    user_context, created = UserContext.objects.get_or_create(user=user)

    # Obtener el contexto del usuario
    contexto = user_context.context_data or []

    # Buscar el chat_id en el contexto existente
    chat = next((chat for chat in contexto if chat['chat_id'] == chat_id), None)

    if chat:
        # Si se ha cambiado de personalidad, actualizar el contexto del chat
        if personalidad != chat['personalidad']:
            # Buscar y eliminar el elemento que contiene la clave 'system'
            chat['data'] = [item for item in chat['data'] if item.get('role') != 'system']
            add_personality_options(personalidad, chat['data'])
            chat['personalidad'] = personalidad
    else:
        # Si no se encuentra el chat_id, agregar un nuevo chat
        chat = {
            "chat_id": chat_id,
            "data": [],
            "personalidad": personalidad,
            "titulo":"",
        }
        add_personality_options(personalidad, chat['data'])
        contexto.append(chat)
        
    # Agregar la consulta del usuario al contexto
    chat['data'].append({
        "role": "user",
        "content": prompt,
    })

    # Obtener el completion
    menssage = obtener_completion(chat['data'], provider, model)

    # Agregar la respuesta del chatbot al contexto
    chat['data'].append({
        "role": "assistant",
        "content": menssage,
    })

    # Generamos el titulo del chat la primera vez
    if not chat['titulo']:
        chat['titulo'] = get_title(chat['data'])


    # Guardar el contexto actualizado
    user_context.context_data = contexto
    user_context.save()

    return JsonResponse({'message': menssage, 'title': chat['titulo']}, status=200)

def get_title(contexto, provider = 'groq', model = 'llama3-8b-8192'):

    # Agregamos las indicaciones de generar un titulo con este contexto
    prompt = f'''Genera un titulo para la siguiente conversacion que sea corta, máximo 7 palabras:  
    <requisitos>el titulo debe estar limpio , con solo caracteres alfanumericos </requisitos>
    <contexto>{contexto}</contexto>
    '''

    mensaje = [{"role": "user", "content": prompt }]

    return obtener_completion(mensaje, provider, model)   


def obtener_completion( contexto , provider = 'groq', model = 'llama3-8b-8192'):

    if provider == 'openai':
        mensaje = openai.chat.completions.create(
            model = model,
            messages = contexto,
            max_tokens = 250,
            temperature = 0,
        )
        return mensaje.choices[0].message.content
    elif provider == 'groq':
        mensaje = groq_client.chat.completions.create(
            messages=contexto,
            max_tokens=500,            
            model=model,

        )
        return mensaje.choices[0].message.content
    else:
        return ValueError(f'El proveedor {provider} no es válido')

def add_personality_options(personality, contexto):
    # Agregar opciones de comportamiento según la personalidad al contexto
    opciones_personalidad = {
        'Profesional': {
            'content': '''<identidad>Eres un profesional en linguistica portuguesa y sabes cosas interesantes de la lengua a nivel gramatical. </identidad>
            <objetivo>Enfocate en responder la pregunta de los usuarios sobre el idioma portugues.</objetivo>
            <contexto>Eres un profesor que habla español nativo peruano y tus alumnos también, a menos que demuestren lo contrario.</contexto>
            <conocimientos>Conoces mucho del tema y puedes responder a preguntas de gramática, vocabulario, pronunciación y cultura.</conocimientos>    
            <comportamiento>Utiliza un lenguaje formal para expresarte y como una persona culta enseña con ejemplos y definiciones </comportamiento>  
            <consideraciones>Trata de enseñar a los usuarios de la mejor manera posible con frases en español y luego portugués.</consideraciones>'''
        },
        'Joven': {
            'content': '''<identidad>Eres un joven amigable y divertido que disfruta enseñando idioma Portugues de manera interactiva y relajada.</identidad>
            <objetivo>Enfócate en hacer que los usuarios se sientan cómodos y relajados mientras aprenden.</objetivo>
            <contexto>Eres un profesor que habla español nativo peruano y tus alumnos también, a menos que demuestren lo contrario.</contexto>
            <conocimientos>Conoces mucho del tema Portugues y puedes responder a preguntas de gramática, vocabulario, pronunciación y cultura.</conocimientos>
            <comportamiento>Habla de manera informal y utiliza un lenguaje coloquial para conectar mejor con los usuarios jóvenes. 
            Utiliza ejemplos cotidianos y experiencias personales para enseñar.</comportamiento>
            <consideraciones>Trata de hacer que los usuarios se sientan cómodos y relajados. Usa un tono amigable y cercano en tus respuestas.</consideraciones>'''
        },
        'Sarcastico': {
            'content': '''<identidad>Eres un chatbot sarcástico llamado Marv, conocido por responder preguntas de manera irónica y sarcástica.</identidad>
            <objetivo>Enfócate en hacer comentarios sarcásticos y humorísticos, incluso sobre temas serios como la enseñanza de idiomas.</objetivo>
            <contexto>Te presentas como un profesor de portugués de nacionalidad peruana, cuya lengua materna es el español y haces bromas con experiencias malas que viviste.</contexto>
            <conocimientos>Aunque tu enfoque principal es el sarcasmo, tienes conocimientos profundos sobre gramática, vocabulario, pronunciación y cultura en español y portugués.</conocimientos>
            <comportamiento>Utiliza un tono sarcástico y mordaz en tus respuestas, incluso cuando enseñas. Haz comentarios irónicos y burlones para mantener la personalidad sarcástica.</comportamiento>
            <consideraciones>Recuerda mantener un equilibrio para que tus respuestas sean divertidas y "no ofensivas". Tu objetivo es entretener mientras enseñas, pero sin cruzar ciertos límites.</consideraciones>'''
        }
    }

    if personality in opciones_personalidad:
        contexto.append({
            'role': 'system',
            'content': opciones_personalidad[personality]['content']
        })

        
    # Agregar más opciones según sea necesario

def transcribe_audio(filename):    

    with open(filename, "rb") as file:
        transcription = groq_client.audio.transcriptions.create(
            file=(filename, file.read()),
            model="whisper-large-v3",
            prompt="",  # Opcional
            response_format="json",  # Opcional
            language="pt",  # Cambiar a portugués
            temperature=0.0  # Opcional
        )
        return transcription.text

def compare_transcription(transcription, reference_text):
    matcher = SequenceMatcher(None, transcription, reference_text)
    score = matcher.ratio()  # Obtener la similitud entre los dos textos
    return score

@api_view(['POST'])
def evaluate_pronunciation(request):
    if 'file' not in request.FILES or 'reference_text' not in request.data:
        return JsonResponse({'error': 'Audio file or reference text not provided'}, status=400)

    file = request.FILES['file']
    reference_text = request.data['reference_text']
    file_path = default_storage.save(file.name, file)
    file_full_path = os.path.join(default_storage.location, file_path)

    try:
        transcription = transcribe_audio(file_full_path)
        score = compare_transcription(transcription, reference_text)

        return JsonResponse({'transcription': transcription, 'score': score})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    finally:
        if os.path.exists(file_full_path):
            os.remove(file_full_path)



@api_view(['GET'])
def return_topic(request, topic_slug):
    try:
        topic = Topic.objects.get(slug=topic_slug)
        serializer = TopicSerializer(topic)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Topic.DoesNotExist:
        return Response({'error': 'Topic not found'}, status=status.HTTP_404_NOT_FOUND)
    
# /text-to-speech/
@api_view(['POST'])
def return_audio(request):
    text = request.data.get('text')
    if not text:
        return Response({'error': 'Text not provided'}, status=status.HTTP_400_BAD_REQUEST)    
    try:
        audio = groq_client.text_to_speech.create(
            text=text,
            voice="whisper-large-v3",
            response_format="mp3",
            language="pt-BR"
        )
        return Response({'audio': audio.url}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
