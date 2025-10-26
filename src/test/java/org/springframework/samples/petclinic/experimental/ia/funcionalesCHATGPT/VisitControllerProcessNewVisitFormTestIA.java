package org.springframework.samples.petclinic.owner;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

/**
 * Caso de prueba funcional para el método processNewVisitForm del controlador.
 *
 * Escenarios cubiertos: 1. Envío válido: se espera redirección a
 * "redirect:/owners/{ownerId}". 2. Envío inválido: se espera retornar la vista
 * "pets/createOrUpdateVisitForm".
 */
@SpringBootTest
@AutoConfigureMockMvc
class VisitControllerProcessNewVisitFormTestIA {

	@Autowired
	private MockMvc mockMvc;

	/**
	 * Escenario exitoso: el formulario se envía correctamente, y se espera redirección al
	 * endpoint del propietario.
	 */
	@Test
	void shouldProcessNewVisitSuccessfully() throws Exception {
		mockMvc
			.perform(post("/owners/{ownerId}/pets/{petId}/visits/new", 1, 1)
				.contentType(MediaType.APPLICATION_FORM_URLENCODED)
				.param("date", "2025-10-25") // campos válidos simulados del formulario
				.param("description", "Routine check-up"))
			.andExpect(status().is3xxRedirection()) // debe redirigir
			.andExpect(redirectedUrl("/owners/1")) // URL esperada
			.andExpect(flash().attributeExists("message")); // mensaje flash presente
	}

	/**
	 * Escenario con error de validación: si falta un campo requerido (por ejemplo, la
	 * descripción), se debe retornar la vista del formulario.
	 */
	@Test
	void shouldReturnFormWhenValidationFails() throws Exception {
		mockMvc
			.perform(post("/owners/{ownerId}/pets/{petId}/visits/new", 1, 1)
				.contentType(MediaType.APPLICATION_FORM_URLENCODED)
				.param("date", "")) // campo vacío para provocar error de validación
			.andExpect(status().isOk()) // no redirige, retorna vista
			.andExpect(view().name("pets/createOrUpdateVisitForm"));
	}

}
