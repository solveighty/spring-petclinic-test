package org.springframework.samples.petclinic.owner;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

import java.time.LocalDate;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;

/**
 * Prueba funcional para el endpoint POST /owners/{ownerId}/pets/new que valida el flujo
 * de creación de una mascota (Pet) en el sistema.
 */
@SpringBootTest
@AutoConfigureMockMvc
class PetControllerProcessCreationFormTestIA {

	@Autowired
	private MockMvc mockMvc;

	/**
	 * Caso de prueba: flujo exitoso de creación de mascota. Debe redirigir correctamente
	 * a /owners/{ownerId}.
	 */
	@Test
	void shouldProcessCreationFormSuccessfully() throws Exception {
		mockMvc
			.perform(post("/owners/{ownerId}/pets/new", 1).param("name", "Firulais")
				.param("birthDate", LocalDate.now().minusYears(2).toString())
				.param("type", "dog")) // Parámetros simulando el formulario
			.andExpect(status().is3xxRedirection()) // Debe redirigir
			.andExpect(redirectedUrl("/owners/1")) // URL esperada
			.andExpect(flash().attributeExists("message")); // Mensaje flash
	}

	/**
	 * Caso de prueba: error de validación por fecha de nacimiento futura. Debe retornar
	 * la vista "pets/createOrUpdatePetForm".
	 */
	@Test
	void shouldReturnFormViewWhenValidationFails() throws Exception {
		mockMvc
			.perform(post("/owners/{ownerId}/pets/new", 1).param("name", "Max")
				.param("birthDate", LocalDate.now().plusDays(5).toString()) // Fecha
																			// futura ->
																			// error
				.param("type", "dog"))
			.andExpect(status().isOk()) // No redirige, muestra el formulario
			.andExpect(view().name("pets/createOrUpdatePetForm")) // Vista esperada
			.andExpect(model().attributeExists("pet")) // Modelo contiene pet
			.andExpect(model().hasErrors()); // Debe tener errores de validación
	}

}
