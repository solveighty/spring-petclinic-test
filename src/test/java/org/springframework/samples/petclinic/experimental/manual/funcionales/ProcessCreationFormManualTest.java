package org.springframework.samples.petclinic.owner;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

import java.beans.Transient;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
class ProcessCreationFormManualTest {

	@Autowired
	private MockMvc mockMvc;

	// Retorna redireccion cuando la mascota se crea exitosamente
	@Test
	void shouldRedirectWhenPetCreatedSuccessfully() throws Exception {
		mockMvc.perform(
				post("/owners/10/pets/new").param("name", "Bol").param("birthDate", "2023-01-15").param("type.id", "1"))
			.andExpect(status().isOk())
			.andExpect(view().name("redirect:/owners/10"))
			.andExpect(model().attributeExists("message"));
	}

	// Retorna redirección cuando la mascota se crea exitosamente con número en el nombre
	@Test
	void shouldRedirectWhenPetCreatedSuccessfullyWithNumberInName() throws Exception {
		mockMvc
			.perform(post("/owners/10/pets/new").param("name", "Bol123")
				.param("birthDate", "2023-01-15")
				.param("type.id", "1"))
			.andExpect(status().isOk())
			.andExpect(view().name("redirect:/owners/10"))
			.andExpect(model().attributeExists("message"));
	}

	// Retorna formulario cuando el nombre de la mascota ya existe
	@Test
	void shouldReturnFormWhenDuplicateName() throws Exception {
		mockMvc.perform(
				post("/owners/10/pets/new").param("name", "Bol").param("birthDate", "2023-01-15").param("type.id", "1"))
			.andExpect(status().isOk())
			.andExpect(view().name("pets/createOrUpdatePetForm"))
			.andExpect(model().attributeHasFieldErrorCode("pet", "name", "duplicate"));
	}

	// Retorna formulario cuando la fecha de nacimiento es invalida
	@Test
	void shouldReturnFormWhenInvalidDate() throws Exception {
		mockMvc.perform(
				post("/owners/10/pets/new").param("name", "Kito").param("birthDate", "2025-01-4").param("type.id", "1"))
			.andExpect(status().isOk())
			.andExpect(view().name("pets/createOrUpdatePetForm"))
			.andExpect(model().attributeHasFieldErrorCode("pet", "birthDate", "typeMismatch.birthDate"));
	}

	// Retorna Internal Server Error cuando el tipo de mascota es invalido
	@Test
	void shouldReturnServerErrorWhenInvalidType() throws Exception {
		mockMvc
			.perform(post("/owners/10/pets/new").param("name", "Loro")
				.param("birthDate", "2023-01-15")
				.param("type.id", "-1"))
			.andExpect(status().isInternalServerError());
	}

	// Retorna Internal Server Error cuando el tipo de mascota no existe
	@Test
	void shouldReturnServerErrorWhenTypeDoesNotExist() throws Exception {
		mockMvc
			.perform(post("/owners/10/pets/new").param("name", "Loro")
				.param("birthDate", "2023-01-15")
				.param("type.id", "8"))
			.andExpect(status().isInternalServerError());
	}

}
