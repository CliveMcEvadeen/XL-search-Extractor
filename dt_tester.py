def physics_form(request):

    # receives data from the post methods of the form

    if request.method == 'POST':
        # Extract data from the POST request
        #converting them to strings such that if the user leaves the  fields empty
        student_name = request.POST.get('student_name')
        subject_name = request.POST.get('subject_name')
        c1 = float(request.POST.get('c1')) if request.POST.get('c1') != '' else None
        c2 = float(request.POST.get('c2')) if request.POST.get('c2') != '' else None
        c3 = float(request.POST.get('c3')) if request.POST.get('c3') != '' else None
        c4 = float(request.POST.get('c4')) if request.POST.get('c4') != '' else None
        final = float(request.POST.get('final')) if request.POST.get('final') != '' else None
        
        # Validate if student exists
        try:
            student_instance = Student.objects.get(name=student_name)
        except Student.DoesNotExist:
            messages.error(request, "Student does not exist")
            # return HttpResponse("Student does not exist")

        # Validate if subject exists
        try:
            subject_instance = Subject.objects.get(name=subject_name)
        except Subject.DoesNotExist:
            messages.error(request, "Subject does not exist")
            # return HttpResponse("Subject does not exist")

        # Process form data and save it
        subject_detail, created = SubjectDetail.objects.get_or_create(
            student=student_instance,
            subject=subject_instance,
            defaults={'c1': c1, 'c2': c2, 'c3': c3, 'c4': c4, 'final': final}
        )

        messages.success(request,"Student records created successfully")
        if not created:
            # Update the existing record
            subject_detail.c1 = c1
            subject_detail.c2 = c2
            subject_detail.c3 = c3
            subject_detail.c4 = c4
            subject_detail.final = final
            subject_detail.save()

            messages.success(request,"Student records updated successfully")

        return redirect('student_mgt')
    else: