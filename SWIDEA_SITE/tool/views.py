from django.shortcuts import render, redirect, get_object_or_404
from .models import DevTool


def tool_list(request):
    """개발툴 리스트 페이지"""
    tools = DevTool.objects.all()
    context = {'tools': tools}
    return render(request, 'tool/tool_list.html', context)


def tool_detail(request, tool_id):
    """개발툴 상세 페이지"""
    tool = get_object_or_404(DevTool, pk=tool_id)
    ideas = tool.ideas.all()

    context = {
        'tool': tool,
        'ideas': ideas,
    }
    return render(request, 'tool/tool_detail.html', context)


def tool_register(request):
    """개발툴 등록 페이지"""
    if request.method == 'POST':
        name = request.POST.get('name')
        kind = request.POST.get('kind')
        content = request.POST.get('content')

        tool = DevTool.objects.create(
            name=name,
            kind=kind,
            content=content
        )

        return redirect('tool:detail', tool_id=tool.id)

    return render(request, 'tool/tool_register.html')


def tool_update(request, tool_id):
    """개발툴 수정 페이지"""
    tool = get_object_or_404(DevTool, pk=tool_id)

    if request.method == 'POST':
        tool.name = request.POST.get('name')
        tool.kind = request.POST.get('kind')
        tool.content = request.POST.get('content')
        tool.save()

        return redirect('tool:detail', tool_id=tool.id)

    context = {'tool': tool}
    return render(request, 'tool/tool_update.html', context)


def tool_delete(request, tool_id):
    """개발툴 삭제"""
    tool = get_object_or_404(DevTool, pk=tool_id)
    if request.method == 'POST':
        tool.delete()
        return redirect('tool:list')
    return redirect('tool:detail', tool_id=tool_id)
