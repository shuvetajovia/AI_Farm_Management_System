import os

land_form_path = r"d:\EY_4.0_AVCOE\Farm_Managemnet (2)\Farm_Managemnet\templates\farmers\land_form.html"
soil_form_path = r"d:\EY_4.0_AVCOE\Farm_Managemnet (2)\Farm_Managemnet\templates\soil\soil_form.html"

land_form_content = r"""{% extends 'base.html' %}
{% load static %}

{% block title %}Land Form - Smart Agriculture{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col-md-8 col-lg-6">
            <div class="glass-card p-5 fade-in">
                <div class="text-center mb-4">
                    <div class="mb-3 d-inline-block p-3 rounded-circle bg-success bg-opacity-10 text-success">
                        <i class="fas fa-map-marked-alt fs-2"></i>
                    </div>
                    <h3 class="fw-bold text-success">{% if form.instance.pk %}Edit Land Details{% else %}Add New Land{% endif %}</h3>
                    <p class="text-secondary">Enter the details of your agricultural land</p>
                </div>

                <form method="post" novalidate>
                    {% csrf_token %}

                    {% for field in form %}
                    <div class="mb-4">
                        <label for="{{ field.id_for_label }}"
                            class="form-label fw-bold text-secondary text-uppercase small ls-1">
                            {{ field.label }}
                        </label>
                        {{ field }}
                        {% if field.help_text %}
                        <div class="form-text small">{{ field.help_text }}</div>
                        {% endif %}
                        {% if field.errors %}
                        <div class="text-danger small mt-1">{{ field.errors.0 }}</div>
                        {% endif %}
                    </div>
                    {% endfor %}

                    <div class="d-grid gap-2 mt-5">
                        <button type="submit" class="btn btn-custom btn-lg shadow-sm">
                            <i class="fas fa-save me-2"></i>Save Details
                        </button>
                        <a href="{% url 'farmers:land_list' %}" class="btn btn-outline-secondary">Cancel</a>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>

<script>
    document.addEventListener('DOMContentLoaded', function () {
        // Add form-control styling to all inputs in the form
        const formInputs = document.querySelectorAll('input, select, textarea');
        formInputs.forEach(input => {
            if (!input.classList.contains('form-control') && !input.classList.contains('form-select')) {
                input.classList.add('form-control');
                input.classList.add('px-3');
                input.classList.add('py-2');
            }
        });
    });
</script>
{% endblock %}"""

soil_form_content = r"""{% extends 'base.html' %}
{% load static %}

{% block title %}Soil Data Form - Smart Agriculture{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col-md-8 col-lg-6">
            <div class="glass-card p-5 fade-in">
                <div class="text-center mb-4">
                    <div class="mb-3 d-inline-block p-3 rounded-circle bg-success bg-opacity-10 text-success">
                        <i class="fas fa-flask fs-2"></i>
                    </div>
                    <h3 class="fw-bold text-success">{% if form.instance.pk %}Edit Soil Data{% else %}Add Soil Data{% endif %}</h3>
                    <p class="text-secondary">Record soil analysis results for precise recommendations</p>
                </div>

                <form method="post" novalidate>
                    {% csrf_token %}

                    {% for field in form %}
                    <div class="mb-4">
                        <label for="{{ field.id_for_label }}"
                            class="form-label fw-bold text-secondary text-uppercase small ls-1">
                            {{ field.label }}
                        </label>

                        <!-- Input Group handling for specific fields like ppm, % -->
                        <div class="input-group">
                            {{ field }}
                            {% if 'nitrogen' in field.name or 'phosphorus' in field.name or 'potassium' in field.name %}
                            <span class="input-group-text bg-light text-secondary small">ppm</span>
                            {% elif 'moisture' in field.name %}
                            <span class="input-group-text bg-light text-secondary small">%</span>
                            {% endif %}
                        </div>

                        {% if field.help_text %}
                        <div class="form-text small">{{ field.help_text }}</div>
                        {% endif %}
                        {% if field.errors %}
                        <div class="text-danger small mt-1">{{ field.errors.0 }}</div>
                        {% endif %}
                    </div>
                    {% endfor %}

                    <div class="d-grid gap-2 mt-5">
                        <button type="submit" class="btn btn-custom btn-lg shadow-sm">
                            <i class="fas fa-save me-2"></i>Save Record
                        </button>
                        <a href="{% url 'soil:list' %}" class="btn btn-outline-secondary">Cancel</a>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>

<script>
    document.addEventListener('DOMContentLoaded', function () {
        // Add form-control styling to all inputs in the form
        const formInputs = document.querySelectorAll('input, select, textarea');
        formInputs.forEach(input => {
            if (!input.classList.contains('form-control') && !input.classList.contains('form-select')) {
                input.classList.add('form-control');
                input.classList.add('px-3');
                input.classList.add('py-2');
            }
        });
    });
</script>
{% endblock %}"""

def write_force(path, content):
    try:
        if os.path.exists(path):
            os.remove(path)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Successfully overwrote {path}")
    except Exception as e:
        print(f"Error writing {path}: {e}")

write_force(land_form_path, land_form_content)
write_force(soil_form_path, soil_form_content)
