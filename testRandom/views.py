from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes



from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status




from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer


@api_view(['GET']) 
@permission_classes([IsAuthenticated])
def generate_test(request):
    
    
    import glob
    import random
    import re
    import json

    # Define the path where the files are located
    files_path = '/home/AsketeP/BackOFTest/files/*.txt'  # Replace with the actual file path pattern
 
    # Initialize variables
    all_questions = []


    # Get file paths using glob
    file_paths = glob.glob(files_path)

    # Iterate over each file
    for file_path in file_paths:
        # Open the file
        with open(file_path, 'r', encoding='utf-8') as file:
            # Initialize variables for each file
            questions = []
            current_question = None
            current_answers = []
            is_question = False

            # Read the file line by line
            for line in file:
                line = line.strip()

                # Skip empty lines
                if not line:
                    continue

                if line == "SOLUCIONES:":
                    break

                # Check if it's a question number
                match = re.match(r'^(\d+)\.', line)
                if match:
                    # Add previous question if it exists
                    if current_question is not None:
                        questions.append({"question": current_question, "answers": current_answers})

                    # Start a new question
                    question_number = match.group(1)
                    current_question = line[len(question_number) + 1:].strip()  # Extract the question text without the prefix
                    current_answers = []
                    is_question = True

                # Check if it's an answer
                elif line.startswith(('a)', 'b)', 'c)')):
                    current_answers.append(line.strip())
                    is_question = False

                # Check if it's a continuation of the question or answer
                elif is_question:
                    current_question += ' ' + line.strip()
                elif current_answers:
                    current_answers[-1] += ' ' + line.strip()

                
            # Add the last question after reaching the end of the file
            if current_question is not None:
                questions.append({"question": current_question, "answers": current_answers})


            # Process the solutions section
            file.seek(0)  # Reset file pointer to the beginning
            content = file.read()
            solutions_start_index = content.find("SOLUCIONES:")
            if solutions_start_index != -1:
                solutions_str = content[solutions_start_index + len("SOLUCIONES:"):].strip()
                solutions = re.findall(r'[a-zA-Z]', solutions_str)
                if len(solutions) == len(questions):
                    for i, solution in enumerate(solutions):
                        questions[i]["solution"] = solution.upper()


            # Append the questions from the current file to the overall list
            all_questions.extend(questions)


    # Select 20 random questions from all files
    random.shuffle(all_questions)
    selected_questions = all_questions[:20]

    # Prepare the data as a dictionary
    data = {
        "questions": [
            {
                "question": question["question"],
                "answers": [answer for answer in question["answers"]],
                "solution": question.get("solution", None)
            }
            for question in selected_questions
        ]
    }

    # Convert the data to JSON string with indentation
    json_data = json.dumps(data)

    # Return the JSON response
    return JsonResponse(json.loads(json_data), json_dumps_params={'indent': 4})








    


@api_view(['POST'])
def register_user(request):
    # Verificar que la solicitud sea de tipo POST
    if request.method == 'POST':
        # Obtener datos del cuerpo de la solicitud
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        tipo = request.data.get('a')
        # Crear un nuevo usuario
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Only POST requests are allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)




class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # You can customize the permissions as needed

    def get_queryset(self):
        return self.queryset.filter(username=self.request.user.username)